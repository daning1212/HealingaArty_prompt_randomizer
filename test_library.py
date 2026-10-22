import copy
import json
from pathlib import Path
import tempfile
import unittest
from compact_library import DEFAULT, HealingArtyPromptLibrary as Node, LibraryStore, ConflictError, parse_config, schema


class CompactTests(unittest.TestCase):
    def config(self, **changes):
        state=copy.deepcopy(DEFAULT);state.update(changes);return json.dumps(state,ensure_ascii=False)

    def test_merge_and_exact_ui_output(self):
        state=json.loads(self.config(prompt='red vest',seed=42,seed_mode='고정'))
        state['selections']['표정']='smiling';state['selections']['헤어스타일']='long hair, straight'
        raw=json.dumps(state);result=Node().generate(raw,'cinematic portrait')
        text=result['result'][0]
        self.assertEqual(text,'cinematic portrait, red vest, long hair, straight, smiling')
        self.assertEqual(result['ui']['prompt'][0],text)
        self.assertEqual(result['ui']['config_used'][0],raw)
        self.assertTrue(result['ui']['text_in_connected'][0])

    def test_empty_and_fixed_random(self):
        self.assertEqual(Node().generate(self.config())['result'][0],'')
        state=json.loads(self.config(seed=42,seed_mode='고정'));state['selections']['의상']='random'
        raw=json.dumps(state);a=Node().generate(raw)['result'];b=Node().generate(raw)['result']
        self.assertEqual(a,b);self.assertNotIn('random',a[0])
        self.assertEqual(Node.IS_CHANGED(raw),Node.IS_CHANGED(raw))

    def test_single_posture_sequential_and_weights(self):
        state=json.loads(self.config(seed=42,seed_mode='고정',posture='앉기',pose='순차'))
        state['weights']['pose']=1.2;raw=json.dumps(state);node=Node()
        first=node.generate(raw)['result'][0];second=node.generate(raw)['result'][0]
        self.assertNotEqual(first,second);self.assertTrue(first.endswith(':1.2)'))
        self.assertIn(schema()['poses']['앉기'][3],first)
        self.assertTrue(Node.IS_CHANGED(raw)!=Node.IS_CHANGED(raw))
        for posture in ['서기','앉기','눕기']:
            text=Node().generate(self.config(posture=posture,pose='random'))['result'][0]
            self.assertTrue(text)

    def test_restored_garments_and_design_counts(self):
        from updated_prompt_randomizer import GARMENT_ADDITIONS
        for category, expected in [('란제리', 229), ('수영복', 200)]:
            pool = schema()['categories'][category][3:]
            self.assertEqual(len(pool), expected)
            self.assertEqual(len(set(pool)), expected)
            self.assertEqual(len(GARMENT_ADDITIONS[category]), 100)
            state = copy.deepcopy(DEFAULT)
            state['seed_mode'] = '고정'
            state['selections'][category] = GARMENT_ADDITIONS[category][0]
            self.assertIn(GARMENT_ADDITIONS[category][0], Node().generate(json.dumps(state))['result'][0])
            state['selections'][category] = 'random'
            self.assertIn(Node().generate(json.dumps(state))['result'][0], pool)
            state['selections'][category] = '순차'
            node = Node()
            self.assertEqual(node.generate(json.dumps(state))['result'][0], pool[0])
            self.assertEqual(node.generate(json.dumps(state))['result'][0], pool[1])
        self.assertTrue(any('sheer camisole' in x for x in GARMENT_ADDITIONS['란제리']))

    def test_invalid_config_and_excluded_categories(self):
        self.assertIn('란제리',schema()['categories']);self.assertIn('수영복',schema()['categories'])
        self.assertNotIn('hair, one side shaved, edgy',schema()['categories']['헤어스타일'])
        for raw in ['null','[]','broken',self.config(seed=1.5),self.config(posture='서기',pose='wrong'),self.config(weights={'표정':float('nan')})]:
            with self.assertRaises(ValueError):parse_config(raw)
        self.assertIsInstance(Node.VALIDATE_INPUTS('broken'),str)


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)/'user'/'prompts.json';self.store=LibraryStore(self.path)
    def tearDown(self):self.tmp.cleanup()
    def change(self,**body):return self.store.change({'revision':self.store.read()['revision'],**body})
    def test_crud_persistence_and_backup(self):
        d=self.change(action='category_add',name='게임');c=d['categories'][0]['id']
        d=self.change(action='save',category_id=c,name='테리 보가드',prompt='red vest, jeans');e=d['selected_id']
        self.assertEqual(LibraryStore(self.path).read()['entries'][0]['prompt'],'red vest, jeans')
        self.change(action='save',id=e,category_id=c,name='테리 보가드',prompt='red cap')
        d=self.change(action='rename',id=e,name='테리');self.assertEqual(d['entries'][0]['name'],'테리')
        self.assertEqual(len(d['entries']),1)
        d=self.change(action='delete',id=e);self.assertEqual(d['entries'],[])
        backup=json.loads(self.path.with_suffix('.json.bak').read_text());self.assertEqual(backup['entries'][0]['name'],'테리')
    def test_duplicates_stale_revision_and_missing_id(self):
        d=self.change(action='category_add',name='게임');c=d['categories'][0]['id']
        with self.assertRaises(ValueError):self.change(action='category_add',name='게임')
        self.change(action='save',category_id=c,name='테리',prompt='text')
        before=self.path.read_bytes()
        with self.assertRaises(ValueError):self.change(action='save',category_id=c,name='테리',prompt='other')
        with self.assertRaises(ConflictError):self.store.change({'revision':0,'action':'delete','id':'x'})
        with self.assertRaises(ValueError):self.change(action='save',id='missing',category_id=c,name='x',prompt='text')
        self.assertEqual(self.path.read_bytes(),before)
    def test_category_delete_cascades_only_selected_and_keeps_backup(self):
        data=self.change(action='category_add',name='게임');first=data['categories'][0]['id']
        data=self.change(action='category_add',name='풍경');second=data['categories'][1]['id']
        self.change(action='save',category_id=first,name='테리',prompt='red vest')
        self.change(action='save',category_id=second,name='산',prompt='mountains')
        self.change(action='save',category_id=first,name='춘리',prompt='blue outfit')
        data=self.change(action='category_delete',id=first)
        self.assertEqual([c['id'] for c in data['categories']],[second])
        self.assertEqual([e['name'] for e in data['entries']],['산'])
        backup=json.loads(self.path.with_suffix('.json.bak').read_text())
        self.assertEqual(len(backup['entries']),3)
        before=self.path.read_bytes()
        with self.assertRaises(ValueError):self.change(action='category_delete',id='missing')
        self.assertEqual(self.path.read_bytes(),before)

    def test_corruption_never_overwritten(self):
        self.path.parent.mkdir(parents=True);self.path.write_text('{broken')
        with self.assertRaises(ValueError):self.change(action='category_add',name='x')
        self.assertEqual(self.path.read_text(),'{broken')

if __name__=='__main__':unittest.main()

class RouteTests(unittest.IsolatedAsyncioTestCase):
    async def test_routes_and_revision_conflict(self):
        import sys, types
        from aiohttp import web
        from aiohttp.test_utils import TestClient, TestServer
        from unittest.mock import patch
        from compact_library import register_routes
        with tempfile.TemporaryDirectory() as tmp:
            routes=web.RouteTableDef()
            modules={'folder_paths':types.SimpleNamespace(get_user_directory=lambda:tmp),
                     'server':types.SimpleNamespace(PromptServer=types.SimpleNamespace(instance=types.SimpleNamespace(routes=routes)))}
            with patch.dict(sys.modules,modules):register_routes()
            app=web.Application();app.add_routes(routes)
            async with TestClient(TestServer(app)) as client:
                response=await client.get('/healingarty/prompt-library/schema');self.assertEqual(response.status,200)
                response=await client.get('/healingarty/prompt-library/data');self.assertEqual((await response.json())['revision'],0)
                response=await client.post('/healingarty/prompt-library/data',json={'action':'category_add','name':'게임','revision':0});self.assertEqual(response.status,200)
                response=await client.post('/healingarty/prompt-library/data',json={'action':'category_add','name':'다른 창','revision':0});self.assertEqual(response.status,409)
                response=await client.post('/healingarty/prompt-library/data',json={'action':'save','revision':1,'category_id':'missing','name':'x','prompt':'text'});self.assertEqual(response.status,400)
                response=await client.get('/healingarty/prompt-library/data');data=await response.json()
                category=data['categories'][0]['id']
                response=await client.post('/healingarty/prompt-library/data',json={'action':'category_delete','revision':1,'id':category});self.assertEqual(response.status,200)
                self.assertEqual((await response.json())['categories'],[])
                self.assertTrue((Path(tmp)/'default'/'healingarty_prompt_library.json').exists())
