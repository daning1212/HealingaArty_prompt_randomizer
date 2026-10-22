"""Compact randomizer and user-owned prompt library. No third-party manager code."""
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import tempfile
import threading
import uuid

try:
    from .updated_prompt_randomizer import HealingArtyPromptRandomizerV11, POSTURE_POSES
except ImportError:
    from updated_prompt_randomizer import HealingArtyPromptRandomizerV11, POSTURE_POSES

CATEGORIES = ('헤어스타일', '표정', '의상', '란제리', '수영복', '신발', '가방', '안경', '모자', '화장', '팬티스타킹')
POSTURES = {'서기': '서서포즈', '앉기': '앉기포즈', '눕기': '누워포즈'}
DEFAULT = {'prompt': '', 'seed': 42, 'seed_mode': '자동', 'posture': 'none', 'pose': 'none',
           'selections': {k: 'none' for k in CATEGORIES}, 'weights': {}, 'category_id': '', 'entry_id': ''}


def schema():
    old = HealingArtyPromptRandomizerV11.INPUT_TYPES()['optional']
    return {'categories': {k: old[k][0] for k in CATEGORIES},
            'poses': {k: ['none', 'random', '순차', *POSTURE_POSES[v]] for k, v in POSTURES.items()}}


def parse_config(raw):
    try:
        value = json.loads(raw)
        if not isinstance(value, dict):
            raise ValueError()
        result = copy.deepcopy(DEFAULT)
        result.update(value)
        if not isinstance(result['prompt'], str) or len(result['prompt']) > 200000:
            raise ValueError()
        if type(result['seed']) is not int or not -1 <= result['seed'] <= 0xffffffffffffffff:
            raise ValueError()
        if result['seed_mode'] not in ('자동', '고정') or result['posture'] not in ('none', *POSTURES):
            raise ValueError()
        spec = schema()
        selections = result['selections']
        if not isinstance(selections, dict) or any(k not in CATEGORIES or v not in spec['categories'][k] for k, v in selections.items()):
            raise ValueError()
        result['selections'] = {k: selections.get(k, 'none') for k in CATEGORIES}
        if result['posture'] != 'none' and result['pose'] not in spec['poses'][result['posture']]:
            raise ValueError()
        weights = result['weights']
        if not isinstance(weights, dict) or any(k not in (*CATEGORIES, 'pose') or type(v) not in (int, float) or not math.isfinite(v) or not .1 <= v <= 2 for k, v in weights.items()):
            raise ValueError()
        return result
    except (ValueError, TypeError, KeyError):
        raise ValueError('랜덤 설정이 잘못되었습니다. 선택값과 시드를 확인하세요.') from None


class HealingArtyPromptLibrary:
    CATEGORY = 'HealingArty'
    RETURN_TYPES = ('STRING', 'STRING', 'INT')
    RETURN_NAMES = ('positive_prompt', '세부사항', '사용된_시드')
    FUNCTION = 'generate'

    def __init__(self):
        self.engine = HealingArtyPromptRandomizerV11()

    @classmethod
    def INPUT_TYPES(cls):
        return {'required': {'config': ('STRING', {'default': json.dumps(DEFAULT, ensure_ascii=False)})},
                'optional': {'text_in': ('STRING', {'forceInput': True})}}

    @classmethod
    def VALIDATE_INPUTS(cls, config, **kwargs):
        try:
            parse_config(config)
            return True
        except ValueError as exc:
            return str(exc)

    @classmethod
    def IS_CHANGED(cls, config, **kwargs):
        state = parse_config(config)
        if state['seed_mode'] == '자동' or state['seed'] == -1 or '순차' in state['selections'].values() or (state['posture'] != 'none' and state['pose'] == '순차'):
            return float('nan')
        return hashlib.sha256(config.encode()).hexdigest()

    def generate(self, config, text_in=''):
        state = parse_config(config)
        values = dict(state['selections'])
        for key, weight in state['weights'].items():
            category = POSTURES.get(state['posture']) if key == 'pose' else key
            if category:
                values[category + '_가중치'] = weight
        if state['posture'] != 'none':
            values[POSTURES[state['posture']]] = state['pose']
        values['text_in'] = ', '.join(v.strip() for v in (text_in or '', state['prompt']) if v.strip())
        result = self.engine.generate(state['seed'], state['seed_mode'], **values)
        if not values['text_in'] and all(v == 'none' for v in state['selections'].values()) and (state['posture'] == 'none' or state['pose'] == 'none'):
            result = ('', result[1], result[2])
        return {'ui': {'prompt': [result[0]], 'details': [result[1]], 'used_seed': [str(result[2])],
                       'config_used': [config], 'text_in_connected': [bool(text_in)]}, 'result': result}


class ConflictError(ValueError):
    pass


class LibraryStore:
    """Whole-file revision checks + atomic replace prevent silent concurrent overwrites."""
    def __init__(self, path):
        self.path = Path(path)
        self.lock = threading.Lock()

    def read(self):
        if not self.path.exists():
            return {'version': 1, 'revision': 0, 'categories': [], 'entries': []}
        try:
            data = json.loads(self.path.read_text(encoding='utf-8'))
            if data.get('version') != 1 or type(data.get('revision')) is not int or not isinstance(data.get('categories'), list) or not isinstance(data.get('entries'), list):
                raise ValueError()
            return data
        except (ValueError, TypeError, AttributeError):
            raise ValueError('보관함 파일을 읽을 수 없습니다. 원본을 보존했습니다. 백업을 확인하세요.') from None

    @staticmethod
    def name(value):
        if not isinstance(value, str) or not value.strip() or len(value.strip()) > 120:
            raise ValueError('이름을 1~120자로 입력하세요.')
        return value.strip()

    def change(self, body):
        with self.lock:
            data = self.read()
            if type(body.get('revision')) is not int or body['revision'] != data['revision']:
                raise ConflictError('다른 창에서 보관함이 변경되었습니다. 새로고침 후 다시 저장하세요. 입력 내용은 유지됩니다.')
            action = body.get('action')
            if action == 'category_add':
                name = self.name(body.get('name'))
                if any(c['name'].casefold() == name.casefold() for c in data['categories']):
                    raise ValueError('같은 이름의 카테고리가 있습니다.')
                data['categories'].append({'id': uuid.uuid4().hex, 'name': name})
            elif action == 'category_delete':
                category = next((c for c in data['categories'] if c['id'] == body.get('id')), None)
                if category is None:
                    raise ValueError('삭제할 카테고리를 선택하세요.')
                data['categories'].remove(category)
                data['entries'] = [e for e in data['entries'] if e['category_id'] != category['id']]
            elif action == 'save':
                category = body.get('category_id')
                if not any(c['id'] == category for c in data['categories']):
                    raise ValueError('저장할 카테고리를 선택하세요.')
                name = self.name(body.get('name'))
                prompt = body.get('prompt')
                if not isinstance(prompt, str) or not prompt.strip() or len(prompt) > 200000:
                    raise ValueError('프롬프트를 입력하세요. 최대 200,000자입니다.')
                entry_id = body.get('id')
                entry = next((e for e in data['entries'] if e['id'] == entry_id), None)
                if entry_id and entry is None:
                    raise ValueError('수정할 항목이 없습니다. 새 항목으로 저장하세요.')
                if any(e['category_id'] == category and e['name'].casefold() == name.casefold() and e['id'] != entry_id for e in data['entries']):
                    raise ValueError('이 카테고리에 같은 이름이 있습니다.')
                if entry is None:
                    entry = {'id': uuid.uuid4().hex}
                    data['entries'].append(entry)
                entry.update(category_id=category, name=name, prompt=prompt)
                data['selected_id'] = entry['id']
            elif action in ('rename', 'delete'):
                entry = next((e for e in data['entries'] if e['id'] == body.get('id')), None)
                if entry is None:
                    raise ValueError('항목을 먼저 선택하세요.')
                if action == 'delete':
                    data['entries'].remove(entry)
                else:
                    name = self.name(body.get('name'))
                    if any(e['category_id'] == entry['category_id'] and e['name'].casefold() == name.casefold() and e['id'] != entry['id'] for e in data['entries']):
                        raise ValueError('같은 이름의 항목이 있습니다.')
                    entry['name'] = name
            else:
                raise ValueError('지원하지 않는 보관함 동작입니다.')
            data['revision'] += 1
            selected = data.pop('selected_id', None)
            self.path.parent.mkdir(parents=True, exist_ok=True)
            if self.path.exists():
                self._atomic(self.path.with_suffix('.json.bak'), self.path.read_text(encoding='utf-8'))
            self._atomic(self.path, json.dumps(data, ensure_ascii=False, indent=2))
            return {**data, 'selected_id': selected}

    @staticmethod
    def _atomic(path, content):
        fd, name = tempfile.mkstemp(dir=path.parent, prefix='.prompt-')
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as stream:
                stream.write(content)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(name, path)
        finally:
            if os.path.exists(name):
                os.unlink(name)


def register_routes():
    import asyncio
    from aiohttp import web
    import folder_paths
    from server import PromptServer
    store = LibraryStore(Path(folder_paths.get_user_directory()) / 'default' / 'healingarty_prompt_library.json')
    routes = PromptServer.instance.routes

    @routes.get('/healingarty/prompt-library/schema')
    async def get_schema(request):
        return web.json_response(schema())

    @routes.get('/healingarty/prompt-library/data')
    async def get_data(request):
        try:
            async with route_lock:
                return web.json_response(await asyncio.to_thread(store.read))
        except (ValueError, OSError) as exc:
            raise web.HTTPBadRequest(text=str(exc)) from exc

    @routes.post('/healingarty/prompt-library/data')
    async def change_data(request):
        try:
            body = await request.json()
            if not isinstance(body, dict):
                raise ValueError('요청 형식이 잘못되었습니다.')
            async with route_lock:
                return web.json_response(await asyncio.to_thread(store.change, body))
        except ConflictError as exc:
            raise web.HTTPConflict(text=str(exc)) from exc
        except (ValueError, OSError) as exc:
            raise web.HTTPBadRequest(text=str(exc)) from exc

    route_lock = asyncio.Lock()
