const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
let document;
class Element{
 constructor(tag){this.tag=tag;this.tagName=tag.toUpperCase();this.children=[];this.style={};this._value='';this.disabled=false;this.readOnly=false;this.handlers={};this.attributes={};}
 append(...items){for(const item of items)if(typeof item==='object')item.parent=this;this.children.push(...items);}replaceChildren(...items){this.children=[];this.append(...items);}
 remove(){if(this.parent)this.parent.children=this.parent.children.filter(c=>c!==this);this.parent=null;}
 get isConnected(){return this===document.body||!!this.parent?.isConnected;}
 set value(v){this._value=String(v);}get value(){return this._value;}
 get selectedIndex(){return this.children.findIndex(c=>c.value===this.value);}set selectedIndex(i){this.value=this.children[i]?.value||'';}
 setAttribute(k,v){this.attributes[k]=v;}addEventListener(type,fn){this.handlers[type]=fn;}
 focus(){document.activeElement=this;}select(){}click(){return this.onclick?.();}
 querySelectorAll(selector){const tags=selector.split(',');return this.children.flatMap(c=>typeof c==='object'?[...(tags.includes(c.tag)?[c]:[]),...c.querySelectorAll(selector)]:[]);}
}
document={createElement:t=>new Element(t),activeElement:null};document.body=new Element('body');
let extension,failNext=false,failSchema=false;
let data={revision:0,categories:[],entries:[]};const clone=x=>JSON.parse(JSON.stringify(x));
const categoryNames=['헤어스타일','표정','의상','란제리','수영복','신발','가방','안경','모자','화장','팬티스타킹'];
const schema={categories:Object.fromEntries(categoryNames.map(k=>[k,['none','random','순차','example']])),poses:{'서기':['none','random','순차','standing'],'앉기':['none','random','순차','sitting'],'눕기':['none','random','순차','lying']}};
let navigationInstalled=0,navigationRemoved=0;
const ctx={installCanvasNavigation(root,getCanvas){navigationInstalled++;assert.ok(root);assert.equal(typeof getCanvas,'function');return ()=>navigationRemoved++;},document,window:{confirm(){throw Error('native confirm forbidden');},prompt(){throw Error('native prompt forbidden');}},navigator:{clipboard:{writeText:async()=>{}}},URL,console,app:{registerExtension:e=>extension=e,canvas:{setDirty(){}}},api:{async fetchApi(path,opts){
 if(failNext){failNext=false;return {ok:false,status:500,text:async()=> 'disk write failed'};}
 if(path.endsWith('/schema')){if(failSchema)return {ok:false,status:404,text:async()=> '404'};return {ok:true,json:async()=>clone(schema)};}
 if(opts){const body=JSON.parse(opts.body);assert.equal(body.revision,data.revision);data=clone(data);
  if(body.action==='category_add')data.categories.push({id:'cat'+data.revision,name:body.name});
  if(body.action==='category_delete'){data.categories=data.categories.filter(c=>c.id!==body.id);data.entries=data.entries.filter(e=>e.category_id!==body.id);}
  if(body.action==='save'){let entry=data.entries.find(e=>e.id===body.id);if(!entry){entry={id:'entry'+data.revision};data.entries.push(entry);}Object.assign(entry,{category_id:body.category_id,name:body.name,prompt:body.prompt});data.selected_id=entry.id;}
  if(body.action==='rename')data.entries.find(e=>e.id===body.id).name=body.name;
  if(body.action==='delete')data.entries=data.entries.filter(e=>e.id!==body.id);
  data.revision++;}return {ok:true,json:async()=>clone(data)};}}};
let source=fs.readFileSync('js/library.js','utf8').replace(/^import .*;\n/gm,'').replace(/export /g,'').replace('import.meta.url',"'http://localhost/library.js'");
vm.createContext(ctx);vm.runInContext(source+'\nglobalThis.Panel=LibraryPanel;',ctx);
function modal(){const overlay=document.body.children.find(e=>e.className==='ha-pl-modal-overlay');assert.ok(overlay,'visible in-page modal expected');return overlay;}
function answer(values={},cancel=false){const overlay=modal();for(const e of overlay.querySelectorAll('input,select'))if(e.attributes['aria-label'] in values)e.value=values[e.attributes['aria-label']];const buttons=overlay.querySelectorAll('button');buttons[cancel?0:1].click();}
async function action(fn,values={},cancel=false){const pending=fn();answer(values,cancel);await pending;assert.equal(document.body.children.filter(e=>e.className==='ha-pl-modal-overlay').length,0);}
(async()=>{
 const widget={name:'config',value:'{}'};const node={widgets:[widget],properties:{},graph:{change(){}}};const p=new ctx.Panel(node);await p.ready;document.body.append(p.root);
 // Actual dialog DOM: empty name validation, then create; no stub prompt/confirm.
 const adding=p.addCategory();answer();assert.ok(p.dialogClose,'empty category name must leave modal open');answer({'카테고리 이름':'게임'});await adding;assert.equal(p.category.value,'cat0');
 p.editor.value='red vest';p.editor.oninput();await action(()=>p.saveEntry(),{'프롬프트 이름':'테리 보가드'});const id=p.state.entry_id;assert.ok(id);assert.equal(p.editor.readOnly,true);
 p.buttons.children[1].click();assert.equal(p.editor.readOnly,false);p.editor.value='red vest, blue jeans';p.editor.oninput();await action(()=>p.saveEntry());assert.equal(data.entries.length,1);
 const raw=widget.value;const restoredNode={widgets:[{name:'config',value:raw}],properties:{},graph:{change(){}}};const restored=new ctx.Panel(restoredNode);await restored.ready;assert.equal(restored.editor.value,'red vest, blue jeans');assert.equal(restored.entries.value,id);
 p.selects['표정'].value='random';p.selects['표정'].onchange();p.executed({prompt:['red vest, blue jeans, smiling'],used_seed:['999'],config_used:[widget.value]});assert.equal(p.output.value,'red vest, blue jeans, smiling');assert.ok(p.resultStatus.textContent.includes('999'));
 p.clear();assert.equal(p.editor.value,'red vest, blue jeans');assert.equal(p.selects['표정'].value,'none');
 p.buttons.children[1].click();p.editor.value='unsaved';p.editor.oninput();await action(()=>p.newEntry(),{},true);assert.equal(p.editor.value,'unsaved');await action(()=>p.choose(id),{},true);assert.equal(p.editor.value,'unsaved');
 // The exact endpoint error must survive subsequent typing/status updates.
 failNext=true;await action(()=>p.saveEntry());assert.equal(p.editor.value,'unsaved');assert.ok(p.error.textContent.includes('disk write failed'));p.name.value='draft';p.name.oninput();assert.equal(p.error.hidden,false);
 await action(()=>p.choose(id));await action(()=>p.rename(),{'새 이름':'테리'});assert.equal(p.name.value,'테리');assert.equal(data.entries[0].name,'테리');
 await action(()=>p.remove(),{},true);assert.equal(data.entries.length,1);await action(()=>p.remove());assert.equal(data.entries.length,0);assert.equal(p.editor.value,'red vest, blue jeans');
 // Save an entry again, delete category with count, cancel first, then delete.
 await action(()=>p.saveEntry(),{'프롬프트 이름':'테리'});const deleting=p.removeCategory();assert.ok(modal().children[0].children.some(e=>e.textContent?.includes('1개')));answer({},true);await deleting;assert.equal(data.categories.length,1);
 await action(()=>p.removeCategory());assert.equal(data.categories.length,0);assert.equal(data.entries.length,0);assert.equal(p.editor.value,'red vest, blue jeans');
 await action(()=>p.newEntry());assert.equal(p.editor.value,'');assert.equal(p.output.value,'red vest, blue jeans, smiling');
 // Modal Escape and node destruction both cancel outstanding actions cleanly.
 const escaped=p.addCategory();modal().handlers.keydown({key:'Escape',stopPropagation(){},preventDefault(){}});await escaped;assert.equal(p.dialogClose,null);
 const pending=p.addCategory();p.destroy();await pending;assert.equal(p.dialogClose,null);
 failSchema=true;const broken=new ctx.Panel({widgets:[{name:'config',value:'{}'}],properties:{}});await broken.ready;assert.ok(broken.error.textContent.includes('재시작'));broken.persist();assert.equal(broken.error.hidden,false);failSchema=false;await broken.refresh();assert.ok(broken.schema);assert.ok(broken.error.hidden);
 class Node{constructor(){this.widgets=[{name:'config',value:'{}'}];this.properties={};this.graph={change(){}};this.size=[850,920];}addDOMWidget(name,type,element,opts){this.dom={element,opts};}setSize(size){this.size=size;}}
 extension.beforeRegisterNodeDef(Node,{name:'HealingArtyPromptLibrary'});const live=new Node();live.onNodeCreated();await live.libraryPanel.ready;assert.equal(live.widgets[0].type,'hidden');assert.equal(live.dom.opts.getHeight,undefined);assert.equal(live.libraryPanel.root.style.height,'100%');assert.equal(live.libraryPanel.root.style.width,'100%');live.onExecuted({prompt:['combined'],used_seed:['42']});assert.equal(live.libraryPanel.output.value,'combined');live.onConfigure();assert.equal(live.libraryPanel.output.value,'combined');live.onRemoved();
 restored.destroy();broken.destroy();assert.equal(navigationInstalled,navigationRemoved);console.log('PASS: in-page modal click/create/save/rename/delete, category deletion/count/cancel, empty-name validation, Escape, draft protection, persistent errors/retry, workflow restore and node lifecycle; native dialogs disabled');
})().catch(e=>{console.error(e);process.exitCode=1;});
