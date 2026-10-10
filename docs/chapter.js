const KEY='ai-atelier.progress.v1';
const moduleId=Number(document.body.dataset.module);
const pages=[...document.querySelectorAll('.page')];
const $=id=>document.getElementById(id);
function read(){
  const raw=localStorage.getItem(KEY);
  const data=raw?JSON.parse(raw):{app:'ai-atelier',version:1,course:'ai-engineering-16-weeks-v1',completed:[],notes:{}};
  if(data.app!=='ai-atelier'||data.version!==1||data.course!=='ai-engineering-16-weeks-v1'||!Array.isArray(data.completed)||data.completed.length>64||data.completed.some(n=>!Number.isInteger(n)||n<0||n>63)||new Set(data.completed).size!==data.completed.length)throw Error('Збережені дані мають неправильний формат. Скористайтеся резервною копією.');
  if(data.notes===undefined)data.notes={};
  if(typeof data.notes!=='object'||Array.isArray(data.notes)||Object.keys(data.notes).length>16||Object.entries(data.notes).some(([id,text])=>!/^(?:[0-9]|1[0-5])$/.test(id)||typeof text!=='string'||text.length>20000))throw Error('Неправильний формат нотаток.');
  return data;
}
function save(update){const data=read();update(data);data.exportedAt=new Date().toISOString();localStorage.setItem(KEY,JSON.stringify(data));}
function sync(){try{const data=read();$('chapterNotes').value=data.notes[moduleId]||'';document.querySelectorAll('[data-step]').forEach(input=>input.checked=data.completed.includes(moduleId*4+Number(input.dataset.step)));$('noteStatus').textContent='Нотатки й прогрес спільні з головною сторінкою.'}catch(e){$('noteStatus').textContent='Не вдалося прочитати дані: '+e.message}}
$('chapterNotes').oninput=()=>{try{save(data=>data.notes[moduleId]=$('chapterNotes').value);$('noteStatus').textContent='Нотатки збережено.'}catch(e){$('noteStatus').textContent='Не збережено: '+e.message}};
document.querySelectorAll('[data-step]').forEach(input=>input.onchange=()=>{try{save(data=>{const steps=new Set(data.completed),id=moduleId*4+Number(input.dataset.step);input.checked?steps.add(id):steps.delete(id);data.completed=[...steps].sort((a,b)=>a-b)});$('noteStatus').textContent='Прогрес збережено.'}catch(e){input.checked=!input.checked;$('noteStatus').textContent='Не збережено: '+e.message}});
let active=0,all=false;
function display(index,changeHash=false){active=Math.max(0,Math.min(pages.length-1,index));pages.forEach((page,i)=>page.hidden=!all&&i!==active);document.querySelectorAll('nav a[data-page]').forEach((a,i)=>{if(i===active)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current')});$('position').textContent=`${active+1} / ${pages.length}`;$('previous').disabled=active===0;$('next').disabled=active===pages.length-1;if(changeHash)history.replaceState(null,'','#page-'+(active+1));}
function hashPage(){const match=location.hash.match(/^#page-(\d+)$/);return match?Number(match[1])-1:0}
document.querySelectorAll('nav a[data-page]').forEach(a=>a.onclick=e=>{e.preventDefault();display(Number(a.dataset.page),true);pages[active].scrollIntoView({block:'start'})});
$('previous').onclick=()=>{display(active-1,true);pages[active].scrollIntoView({block:'start'})};$('next').onclick=()=>{display(active+1,true);pages[active].scrollIntoView({block:'start'})};
$('showAll').onclick=()=>{all=!all;$('showAll').textContent=all?'Посторінково':'Показати весь розділ';display(active)};
$('print').onclick=()=>window.print();window.addEventListener('hashchange',()=>display(hashPage()));
window.addEventListener('storage',e=>{if(e.key===KEY||e.key===null)sync()});
sync();display(hashPage());
