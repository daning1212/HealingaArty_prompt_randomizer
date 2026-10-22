const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
class Element{
 constructor(tag){this.tag=tag;this.children=[];this.style={};this._value='';this.disabled=false;this.readOnly=false;this.handlers={};}
 append(...items){this.children.push(...items);}replaceChildren(...items){this.children=items;}
 set value(v){this._value=String(v);}get value(){return this._value;}
 get selectedIndex(){return this.children.findIndex(c=>c.value===this.value);}set selectedIndex(i){this.value=this.children[i]?.value||'';}
 setAttribute(){}addEventListener(type,fn){this.handlers[type]=fn;}focus(){}select(){}
 querySelectorAll(selector){const tags=selector.split(',');return this.children.flatMap(c=>typeof c==='object'?[...(tags.includes(c.tag)?[c]:[]),...c.querySelectorAll(selector)]:[]);}
}
let extension,confirmResult=true,promptValue='ゲーム',failNext=false;
let data={revision:0,categories:[],entries:[]};const clone=x=>JSON.parse(JSON.stringify(x));
const categoryNames=['헤어스타일','표정','의상','신발','가방','안경','모자','화장','팬티스타킹'];
const schema={categories:Object.fromEntries(categoryNames.map(k=>[k,['none','random','순차','example']])),poses:{'서기':['none','random','순차','standing'],'앉기':['none','random','순차','sitting'],'눕기':['none','random','순차','lying']}};
const ctx={document:{createElement:t=>new Element(t)},window:{confirm:()=>confirmResult,prompt:()=>promptValue},navigator:{clipboard:{writeText:async()=>{}}},URL,console,app:{registerExtension:e=>extension=e,canvas:{setDirty(){}}},api:{async fetchApi(path,opts){if(failNext){failNext=false;return {ok:false,text:async()=> 'disk write failed'};}if(path.endsWith('/schema'))return {ok:true,json:async()=>clone(schema)};
 if(opts){const body=JSON.parse(opts.body);assert.equal(body.revision,data.revision);data=clone(data);if(body.action==='category_add')data.categories.push({id:'cat'+data.revision,name:body.name});
 if(body.action==='save'){let entry=data.entries.find(e=>e.id===body.id);if(!entry){entry={id:'entry'+data.revision};data.entries.push(entry);}Object.assign(entry,{category_id:body.category_id,name:body.name,prompt:body.prompt});data.selected_id=entry.id;}
 if(body.action==='rename')data.entries.find(e=>e.id===body.id).name=body.name;
 if(body.action==='delete')data.entries=data.entries.filter(e=>e.id!==body.id);
 data.revision++;}return {ok:true,json:async()=>clone(data)};}}};
let source=fs.readFileSync('js/library.js','utf8').replace(/^import .*;\n/gm,'').replace(/export /g,'').replace('import.meta.url',"'http://localhost/library.js'");
vm.createContext(ctx);vm.runInContext(source+'\nglobalThis.Panel=LibraryPanel;',ctx);
(async()=>{
 const widget={name:'config',value:'{}'};const node={widgets:[widget],properties:{},graph:{change(){}}};const p=new ctx.Panel(node);await p.ready;
 promptValue='게임';await p.addCategory();assert.equal(p.category.value,'cat0');
 p.name.value='테리 보가드';p.name.oninput();p.editor.value='red vest';p.editor.oninput();await p.saveEntry();const id=p.state.entry_id;assert.ok(id);assert.equal(p.editor.readOnly,true);
 p.buttons.children[1].onclick();assert.equal(p.editor.readOnly,false);p.editor.value='red vest, blue jeans';p.editor.oninput();await p.saveEntry();assert.equal(data.entries.length,1);
 const raw=widget.value;const restoredNode={widgets:[{name:'config',value:raw}],properties:{},graph:{change(){}}};const restored=new ctx.Panel(restoredNode);await restored.ready;assert.equal(restored.editor.value,'red vest, blue jeans');assert.equal(restored.entries.value,id);
 p.selects['표정'].value='random';p.selects['표정'].onchange();p.executed({prompt:['red vest, blue jeans, smiling'],used_seed:['999'],config_used:[widget.value]});assert.equal(p.output.value,'red vest, blue jeans, smiling');assert.ok(p.resultStatus.textContent.includes('999'));
 p.clear();assert.equal(p.editor.value,'red vest, blue jeans');assert.equal(p.selects['표정'].value,'none');assert.ok(p.resultStatus.textContent.includes('마지막 실행'));
 p.buttons.children[1].onclick();p.editor.value='unsaved';p.editor.oninput();confirmResult=false;p.newEntry();assert.equal(p.editor.value,'unsaved');p.choose(id);assert.equal(p.editor.value,'unsaved');
 failNext=true;await p.saveEntry();assert.equal(p.editor.value,'unsaved');assert.ok(p.status.textContent.includes('disk write failed'));
 confirmResult=true;p.choose(id);promptValue='테리';await p.rename();assert.equal(p.name.value,'테리');assert.equal(data.entries[0].name,'테리');
 confirmResult=false;await p.remove();assert.equal(data.entries.length,1);confirmResult=true;await p.remove();assert.equal(data.entries.length,0);assert.equal(p.editor.value,'red vest, blue jeans');
 p.newEntry();assert.equal(p.editor.value,'');assert.equal(p.output.value,'red vest, blue jeans, smiling');
 class Node{constructor(){this.widgets=[{name:'config',value:'{}'}];this.properties={};this.graph={change(){}};this.size=[850,920];}addDOMWidget(name,type,element,opts){this.dom={element,opts};}setSize(size){this.size=size;}}
 extension.beforeRegisterNodeDef(Node,{name:'HealingArtyPromptLibrary'});const live=new Node();live.onNodeCreated();await live.libraryPanel.ready;assert.equal(live.widgets[0].type,'hidden');assert.equal(live.dom.opts.serialize,false);live.onExecuted({prompt:['combined'],used_seed:['42']});assert.equal(live.libraryPanel.output.value,'combined');live.onConfigure();assert.equal(live.libraryPanel.output.value,'combined');live.onRemoved();assert.ok(live.libraryPanel.destroyed);
 p.destroy();restored.destroy();console.log('PASS: library category/create/edit/save/rename/delete, discard protection, failed save preserves draft, workflow restore, output merge display, clear preservation and node lifecycle');
})().catch(e=>{console.error(e);process.exitCode=1;});
