import { app } from '../../scripts/app.js';
import { api } from '../../scripts/api.js';

const TYPE='HealingArtyPromptLibrary';
const LABELS={'헤어스타일':'헤어','표정':'표정','의상':'의상','신발':'신발','가방':'가방','안경':'안경','모자':'모자','화장':'화장','팬티스타킹':'팬티스타킹'};
const INITIAL={prompt:'',seed:42,seed_mode:'자동',posture:'none',pose:'none',selections:Object.fromEntries(Object.keys(LABELS).map(k=>[k,'none'])),weights:{},category_id:'',entry_id:'',entry_name:''};
const clone=v=>JSON.parse(JSON.stringify(v));
function el(tag,cls,text){const e=document.createElement(tag);if(cls)e.className=cls;if(text)e.textContent=text;return e;}
function button(text,fn,cls=''){const e=el('button',cls,text);e.type='button';e.onclick=fn;return e;}
function options(select,values,value){select.replaceChildren();for(const item of values){const [v,label]=Array.isArray(item)?item:[item,item];const o=el('option','',label);o.value=v;select.append(o);}select.value=value;if(select.selectedIndex<0)select.selectedIndex=0;}
async function request(path,body){const r=await api.fetchApi('/healingarty/prompt-library/'+path,body?{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}:undefined);if(!r.ok){const detail=await r.text();throw new Error(r.status===404?'보관함 API를 찾지 못했습니다. ComfyUI 재시작 후 Ctrl+F5를 눌러주세요.':detail||('요청 실패: '+r.status));}return r.json();}
export function readState(raw){const state={...clone(INITIAL),...JSON.parse(raw||'{}')};state.selections={...INITIAL.selections,...state.selections};state.weights={...state.weights};return state;}

export class LibraryPanel{
  constructor(node){
    this.node=node;this.state=readState(this.widget()?.value);this.data={revision:0,categories:[],entries:[]};this.schema=null;this.dataReady=false;this.busy=false;this.editing=!this.state.entry_id;
    this.root=el('div','ha-pl');const title=el('div','ha-pl-title');title.append(el('span','ha-pl-dice','⚄'),el('strong','','HealingArty · Prompt Library'),el('small','','v1.0.1'));this.root.append(title);
    const controls=el('section','ha-pl-section');this.grid=el('div','ha-pl-grid');controls.append(this.grid);
    this.selects={};for(const key of ['헤어스타일','의상','표정','신발','가방']){const select=el('select');select.setAttribute('aria-label',LABELS[key]);select.onchange=()=>{this.state.selections[key]=select.value;this.persist();};this.selects[key]=select;this.grid.append(this.field(LABELS[key],select));}
    this.posture=el('select');options(this.posture,['none','서기','앉기','눕기'],this.state.posture);this.posture.onchange=()=>{this.state.posture=this.posture.value;this.state.pose='none';this.renderPoses();this.persist();};this.grid.append(this.field('자세 유형',this.posture));
    this.pose=el('select');this.pose.onchange=()=>{this.state.pose=this.pose.value;this.persist();};this.grid.append(this.field('포즈',this.pose));
    const extras=el('details');extras.append(el('summary','','액세서리 더 보기'));this.extraGrid=el('div','ha-pl-grid');for(const key of ['안경','모자','화장','팬티스타킹']){const select=el('select');select.onchange=()=>{this.state.selections[key]=select.value;this.persist();};this.selects[key]=select;this.extraGrid.append(this.field(key,select));}extras.append(this.extraGrid);this.grid.append(extras);
    const run=el('div','ha-pl-row');this.seed=el('input');this.seed.type='number';this.seed.min='-1';this.seed.max=String(Number.MAX_SAFE_INTEGER);this.seed.step='1';this.seed.oninput=()=>{const n=Number(this.seed.value);if(this.seed.value===''||!Number.isSafeInteger(n)||n< -1){this.status.textContent='시드는 -1 이상 안전한 정수로 입력하세요. 마지막 유효값을 유지합니다.';return;}this.state.seed=n;this.persist();};
    this.mode=el('select');options(this.mode,['자동','고정'],this.state.seed_mode);this.mode.onchange=()=>{this.state.seed_mode=this.mode.value;this.persist();};
    run.append(this.field('시드',this.seed),this.field('시드 모드',this.mode),button('전체 해제',()=>this.clear()));
    this.advanced=el('details');this.advanced.append(el('summary','','고급 설정 · 가중치'));this.weights=el('div','ha-pl-grid');this.weightInputs={};for(const key of [...Object.keys(LABELS),'pose']){const input=el('input');input.type='number';input.min='.1';input.max='2';input.step='.1';input.oninput=()=>{const n=Number(input.value);if(input.value===''||n<.1||n>2||!Number.isFinite(n)){this.status.textContent='가중치는 0.1~2로 입력하세요. 마지막 유효값을 유지합니다.';return;}this.state.weights[key]=n;this.persist();};this.weightInputs[key]=input;this.weights.append(this.field((LABELS[key]||'포즈')+' 가중치',input));}this.advanced.append(this.weights);controls.append(run,this.advanced);this.root.append(controls);
    const result=el('section','ha-pl-section');const resultHead=el('div','ha-pl-row');resultHead.append(el('strong','','최종 출력 · 보관 프롬프트 + 선택 결과'),button('복사',()=>this.copy()));this.output=el('textarea','ha-pl-output');this.output.readOnly=true;this.output.setAttribute('aria-label','최종 출력');this.resultStatus=el('small','','생성 실행 후 결과가 표시됩니다.');result.append(resultHead,this.output,this.resultStatus);this.root.append(result);
    const library=el('section','ha-pl-section');const head=el('div','ha-pl-row');this.search=el('input');this.search.placeholder='이름 · 내용 검색';this.search.oninput=()=>this.renderEntries();head.append(el('strong','','프롬프트 보관함'),this.search,button('새로고침',()=>this.refresh()));library.append(head);
    this.category=el('select');this.category.onchange=async()=>{const prev=this.state.category_id;if(!await this.discard()){this.category.value=prev;return;}this.state.category_id=this.category.value;this.state.entry_id='';this.state.entry_name='';this.state.prompt='';this.editing=true;this.syncEditor();this.persist();this.renderEntries();};
    const cats=el('div','ha-pl-row');cats.append(this.field('카테고리',this.category),button('+ 카테고리 추가',()=>this.addCategory()),button('카테고리 삭제',()=>this.removeCategory(),'ha-pl-delete'));library.append(cats);
    this.entries=el('select');this.entries.setAttribute('aria-label','저장 목록');this.entries.onchange=()=>this.choose(this.entries.value);library.append(this.field('저장 목록',this.entries));
    this.name=el('input');this.name.placeholder='저장할 이름';this.name.maxLength=120;this.name.oninput=()=>{this.state.entry_name=this.name.value;this.persist();};library.append(this.field('이름',this.name));
    this.editor=el('textarea','ha-pl-editor');this.editor.maxLength=200000;this.editor.placeholder='프롬프트를 입력하거나 저장 목록에서 선택하세요.';this.editor.setAttribute('aria-label','저장 프롬프트');this.editor.oninput=()=>{this.state.prompt=this.editor.value;this.persist();};library.append(this.field('저장 프롬프트',this.editor));
    this.buttons=el('div','ha-pl-row');this.buttons.append(button('+ 새 프롬프트',()=>this.newEntry()),button('수정',()=>{this.editing=true;this.syncEditor();this.editor.focus();}),button('프롬프트 저장',()=>this.saveEntry(),'ha-pl-primary'),button('이름 변경',()=>this.rename()),button('프롬프트 삭제',()=>this.remove(),'ha-pl-delete'));library.append(this.buttons);
    this.status=el('div','ha-pl-status','보관함 불러오는 중…');this.status.setAttribute('role','status');this.error=el('div','ha-pl-error');this.error.setAttribute('role','alert');this.error.hidden=true;library.append(this.status,this.error);this.root.append(library);
    for(const event of ['pointerdown','mousedown','pointerup','mouseup','click','dblclick','wheel','keydown'])this.root.addEventListener(event,e=>e.stopPropagation());
    this.restore();this.ready=this.initialize();
  }
  widget(){return this.node.widgets?.find(w=>w.name==='config');}
  field(label,input){const row=el('label','ha-pl-field');row.append(el('span','',label),input);return row;}
  persist(){const w=this.widget();if(w){w.value=JSON.stringify(this.state);w.callback?.(w.value);}this.node.graph?.change?.();app.canvas.setDirty(true,true);this.resultStatus.textContent='설정 변경됨 · 위 결과는 마지막 실행 값입니다.';this.status.textContent=this.dirty()?'편집 중 · 보관함에 반영하려면 저장하세요.':'현재 문구와 선택값은 다음 생성에 반영됩니다.';}
  restore(){try{this.state=readState(this.widget()?.value);}catch{this.state=clone(INITIAL);this.status.textContent='설정을 읽을 수 없습니다. 입력값을 확인하세요.';}this.editing=!this.state.entry_id;this.syncControls();this.syncEditor();if(this.schema){this.renderCategories();this.renderEntries();}const last=this.node.properties?.haLibraryResult;if(last){this.output.value=last.prompt||'';this.resultStatus.textContent='마지막 실행 결과 · 사용 시드 '+(last.seed||'');}else this.output.value='';}
  syncControls(){for(const [key,select] of Object.entries(this.selects)){if(this.schema)options(select,this.schema.categories[key],this.state.selections[key]);}this.posture.value=this.state.posture;this.renderPoses();this.seed.value=String(this.state.seed);this.mode.value=this.state.seed_mode;for(const [key,input]of Object.entries(this.weightInputs))input.value=String(this.state.weights[key]??1);}
  syncEditor(){this.name.value=this.state.entry_name||'';this.editor.value=this.state.prompt;this.name.readOnly=!this.editing;this.editor.readOnly=!this.editing;}
  renderPoses(){options(this.pose,this.schema?.poses[this.state.posture]||['none'],this.state.pose);this.pose.disabled=this.state.posture==='none';}
  renderCategories(){options(this.category,[['','카테고리 선택'],...this.data.categories.map(c=>[c.id,c.name])],this.state.category_id);}
  renderEntries(){const q=this.search.value.trim().toLowerCase();const list=this.data.entries.filter(e=>e.category_id===this.state.category_id&&(!q||(e.name+' '+e.prompt).toLowerCase().includes(q)));options(this.entries,[['','항목 선택'],...list.map(e=>[e.id,e.name])],this.state.entry_id);}
  dirty(){const e=this.data.entries.find(e=>e.id===this.state.entry_id);return this.editing&&(e?e.prompt!==this.state.prompt||e.name!==this.state.entry_name:!!(this.state.prompt||this.state.entry_name));}
  ask(spec){
    if(this.dialogClose||this.destroyed)return Promise.resolve(null);
    return new Promise(resolve=>{
      const overlay=el('div','ha-pl-modal-overlay');const dialog=el('div','ha-pl-modal');
      dialog.setAttribute('role','dialog');dialog.setAttribute('aria-modal','true');dialog.setAttribute('aria-label',spec.title);
      const previous=document.activeElement;const inputs={};dialog.append(el('strong','ha-pl-modal-title',spec.title));
      if(spec.body)dialog.append(el('p','',spec.body));
      for(const field of spec.fields||[]){
        const input=el(field.options?'select':'input');input.setAttribute('aria-label',field.label);
        if(field.options)options(input,field.options,field.value);else{input.value=field.value||'';input.maxLength=120;}
        inputs[field.key]=input;dialog.append(this.field(field.label,input));
      }
      const validation=el('div','ha-pl-error');validation.setAttribute('role','alert');dialog.append(validation);
      const finish=value=>{overlay.remove();this.dialogClose=null;if(previous?.isConnected)previous.focus();resolve(value);};
      const cancel=button('취소',()=>finish(null));const accept=button(spec.confirmText||'확인',()=>{
        const values=Object.fromEntries(Object.entries(inputs).map(([key,input])=>[key,input.value.trim()]));
        if(Object.values(values).some(v=>!v)){validation.textContent='이름과 카테고리를 입력·선택하세요.';return;}
        finish(values);
      },spec.danger?'ha-pl-delete':'ha-pl-primary');
      const actions=el('div','ha-pl-modal-actions');actions.append(cancel,accept);dialog.append(actions);overlay.append(dialog);
      for(const name of ['pointerdown','mousedown','pointerup','mouseup','click','dblclick','wheel'])overlay.addEventListener(name,e=>e.stopPropagation());
      overlay.addEventListener('keydown',e=>{
        e.stopPropagation();
        if(e.key==='Escape'){e.preventDefault();finish(null);}
        if(e.key==='Enter'&&Object.values(inputs).includes(e.target)&&e.target.tagName!=='SELECT'){e.preventDefault();accept.click();}
        if(e.key==='Tab'){const focusable=[...Object.values(inputs),cancel,accept];const i=focusable.indexOf(document.activeElement);
          const next=e.shiftKey?(i<=0?focusable.length-1:i-1):(i+1)%focusable.length;e.preventDefault();focusable[next].focus();}
      });
      this.dialogClose=()=>finish(null);document.body.append(overlay);(Object.values(inputs)[0]||cancel).focus();
    });
  }
  async discard(){return !this.dirty()||!!await this.ask({title:'편집 내용 확인',body:'저장하지 않은 내용이 있습니다. 버리고 이동할까요?',confirmText:'버리고 이동'});}
  async choose(id){if(!await this.discard()){this.renderEntries();return;}const e=this.data.entries.find(e=>e.id===id);if(!e){this.renderEntries();return;}Object.assign(this.state,{entry_id:e.id,entry_name:e.name,category_id:e.category_id,prompt:e.prompt});this.editing=false;this.syncEditor();this.persist();this.status.textContent='불러옴: '+e.name+' · 생성하면 랜덤 선택과 합쳐 출력합니다.';}
  async newEntry(){if(!await this.discard())return;Object.assign(this.state,{entry_id:'',entry_name:'',prompt:''});this.editing=true;this.syncEditor();this.renderEntries();this.persist();this.name.focus();this.status.textContent='새 프롬프트 · 문구를 입력한 뒤 프롬프트 저장을 누르세요.';}
  clear(){for(const key of Object.keys(this.state.selections))this.state.selections[key]='none';this.state.posture='none';this.state.pose='none';this.syncControls();this.persist();}
  showError(message){this.error.textContent=message;this.error.hidden=false;}
  clearError(){this.error.textContent='';this.error.hidden=true;}
  async initialize(){
    const results=await Promise.allSettled([request('schema'),request('data')]);if(this.destroyed)return;
    if(results[0].status==='fulfilled'){this.schema=results[0].value;this.syncControls();}
    if(results[1].status==='fulfilled'){this.data=results[1].value;this.dataReady=true;this.renderCategories();this.renderEntries();}
    const failed=results.filter(r=>r.status==='rejected');
    if(failed.length){this.showError('보관함 연결 실패: '+failed.map(r=>r.reason.message).join(' / '));this.status.textContent='새로고침으로 다시 연결할 수 있습니다.';}
    else{this.clearError();this.status.textContent='목록 선택으로 불러오기 · 새 프롬프트 작성 후 프롬프트 저장';}
  }
  async refresh(){if(!this.schema||!this.dataReady){await this.initialize();return;}try{const data=await request('data');if(this.destroyed)return;this.data=data;this.clearError();this.renderCategories();this.renderEntries();this.status.textContent='목록 갱신 완료 · 편집 내용은 유지했습니다.';}catch(e){this.showError(e.message);}}
  async mutate(body){
    if(this.busy){this.showError('저장 작업 중입니다. 잠시 후 다시 눌러주세요.');return null;}
    if(!this.dataReady){this.showError('보관함이 연결되지 않았습니다. 새로고침을 누르세요.');return null;}
    this.busy=true;const locked=[...this.root.querySelectorAll('button,input,select,textarea')].map(e=>[e,e.disabled]);for(const [e]of locked)e.disabled=true;
    try{const data=await request('data',{...body,revision:this.data.revision});if(this.destroyed)return null;this.data=data;this.clearError();this.renderCategories();this.renderEntries();return data;}
    catch(e){this.showError(e.message);this.status.textContent='실패 · 입력 내용은 유지됩니다.';return null;}
    finally{this.busy=false;for(const [e,disabled]of locked)e.disabled=disabled;}
  }
  async addCategory(){
    const answer=await this.ask({title:'새 카테고리',fields:[{key:'name',label:'카테고리 이름'}],confirmText:'추가'});if(!answer)return;
    const data=await this.mutate({action:'category_add',name:answer.name});if(data){
      // Do not discard a draft merely to create a category.
      if(!this.state.entry_id){this.state.category_id=data.categories.at(-1).id;this.renderCategories();this.renderEntries();this.persist();}
      this.status.textContent='카테고리를 추가했습니다.';
    }
  }
  async removeCategory(){
    const c=this.data.categories.find(c=>c.id===this.state.category_id);if(!c){this.showError('삭제할 카테고리를 선택하세요.');return;}
    const count=this.data.entries.filter(e=>e.category_id===c.id).length;
    const ok=await this.ask({title:'카테고리 삭제',body:'「'+c.name+'」 카테고리와 안의 프롬프트 '+count+'개를 삭제할까요? 현재 편집 문구는 남겨둡니다.',confirmText:'카테고리 삭제',danger:true});if(!ok)return;
    const data=await this.mutate({action:'category_delete',id:c.id});if(data){Object.assign(this.state,{category_id:'',entry_id:'',entry_name:''});this.editing=true;this.syncEditor();this.renderCategories();this.renderEntries();this.persist();this.status.textContent='카테고리를 삭제했습니다. 현재 편집 문구는 유지했습니다.';}
  }
  async saveEntry(){
    if(!this.state.prompt.trim()){this.showError('저장할 프롬프트를 먼저 입력하세요.');this.editing=true;this.syncEditor();this.editor.focus();return;}
    if(!this.dataReady){this.showError('보관함이 연결되지 않았습니다. 새로고침을 누르세요.');return;}
    if(!this.data.categories.length){this.showError('먼저 + 카테고리 추가로 카테고리를 만드세요.');return;}
    const answer=await this.ask({title:'프롬프트 저장',fields:[{key:'category_id',label:'카테고리',value:this.state.category_id,options:this.data.categories.map(c=>[c.id,c.name])},{key:'name',label:'프롬프트 이름',value:this.state.entry_name}],confirmText:'저장'});if(!answer)return;
    const data=await this.mutate({action:'save',id:this.state.entry_id||null,category_id:answer.category_id,name:answer.name,prompt:this.state.prompt});if(data){const e=data.entries.find(e=>e.id===data.selected_id);Object.assign(this.state,{category_id:e.category_id,entry_id:e.id,entry_name:e.name,prompt:e.prompt});this.editing=false;this.syncEditor();this.renderCategories();this.renderEntries();this.persist();this.status.textContent='저장됨: '+e.name;}
  }
  async rename(){
    const e=this.data.entries.find(e=>e.id===this.state.entry_id);if(!e){this.showError('이름을 바꿀 항목을 선택하세요.');return;}
    const answer=await this.ask({title:'이름 변경',fields:[{key:'name',label:'새 이름',value:this.state.entry_name||e.name}],confirmText:'변경'});if(!answer)return;
    const data=await this.mutate({action:'rename',id:e.id,name:answer.name});if(data){this.state.entry_name=data.entries.find(v=>v.id===e.id).name;this.syncEditor();this.renderEntries();this.persist();this.status.textContent='이름을 변경했습니다. 편집 중인 문구는 유지했습니다.';}
  }
  async remove(){
    const e=this.data.entries.find(e=>e.id===this.state.entry_id);if(!e){this.showError('삭제할 프롬프트를 선택하세요.');return;}
    const ok=await this.ask({title:'프롬프트 삭제',body:'「'+e.name+'」을 삭제할까요? 현재 편집 문구는 남겨둡니다.',confirmText:'삭제',danger:true});if(!ok)return;
    const data=await this.mutate({action:'delete',id:e.id});if(data){Object.assign(this.state,{entry_id:'',entry_name:''});this.editing=true;this.syncEditor();this.renderEntries();this.persist();this.status.textContent='프롬프트를 삭제했습니다. 현재 문구는 유지했습니다.';}
  }
  executed(message){const prompt=message?.prompt?.[0];if(typeof prompt!=='string')return;this.output.value=prompt;const seed=message.used_seed?.[0]??'';this.node.properties??={};this.node.properties.haLibraryResult={prompt,seed};const changed=message.config_used?.[0]!==this.widget()?.value;this.resultStatus.textContent=(changed?'이전 설정의 실행 결과':'마지막 실행 결과')+' · 사용 시드 '+seed+(message.text_in_connected?.[0]?' · text_in 포함':'');}
  async copy(){try{await navigator.clipboard.writeText(this.output.value);this.status.textContent='최종 출력을 복사했습니다.';}catch{this.output.focus();this.output.select();this.status.textContent='자동 복사가 제한되었습니다. Ctrl+C로 복사하세요.';}}
  destroy(){this.destroyed=true;this.dialogClose?.();}
}

app.registerExtension({name:'HealingArty.PromptLibrary',async setup(){const link=el('link');link.rel='stylesheet';link.href=new URL('./library.css?v=1.0.1',import.meta.url).href;document.head.append(link);},beforeRegisterNodeDef(Node,data){if(data.name!==TYPE)return;
  const created=Node.prototype.onNodeCreated;Node.prototype.onNodeCreated=function(){const result=created?.apply(this,arguments);this.resizable=true;const w=this.widgets?.find(w=>w.name==='config');if(w){w.type='hidden';w.computeSize=()=>[0,-4];w.draw=()=>{};}
    this.libraryPanel=new LibraryPanel(this);this.syncLibrarySize=()=>{const style=this.libraryPanel.root.style;style.width=Math.max(420,this.size[0]-20)+'px';style.height=Math.max(480,this.size[1]-65)+'px';};
    this.addDOMWidget('library','healingarty-library',this.libraryPanel.root,{serialize:false,hideOnZoom:false,selectOn:[],getMinHeight:()=>480,getHeight:()=>Math.max(480,this.size[1]-65),onDraw:()=>this.syncLibrarySize(),afterResize:()=>this.syncLibrarySize()});this.setSize([850,920]);this.syncLibrarySize();return result;};
  const configured=Node.prototype.onConfigure;Node.prototype.onConfigure=function(){const r=configured?.apply(this,arguments);this.libraryPanel?.restore();return r;};
  const executed=Node.prototype.onExecuted;Node.prototype.onExecuted=function(message){const r=executed?.apply(this,arguments);this.libraryPanel?.executed(message);return r;};
  const removed=Node.prototype.onRemoved;Node.prototype.onRemoved=function(){this.libraryPanel?.destroy();return removed?.apply(this,arguments);};
}});
