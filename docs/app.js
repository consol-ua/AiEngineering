const STORAGE_KEY='ai-atelier.progress.v1';
let completed=new Set(),filter='all',storageWarning='';
const $=id=>document.getElementById(id);
let toastTimer;
function toast(message){$('toast').textContent=message;$('toast').hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('toast').hidden=true,6000)}
function validateBackup(data){
  if(!data||data.app!=='ai-atelier'||data.version!==1||data.course!=='ai-engineering-16-weeks-v1'||!Array.isArray(data.completed)||data.completed.length>64||data.completed.some(id=>!Number.isInteger(id)||id<0||id>=64)||new Set(data.completed).size!==data.completed.length){throw Error('Неправильний формат резервної копії. Потрібен JSON AI Atelier версії 1.')}
  return new Set(data.completed);
}
function snapshot(steps){return {app:'ai-atelier',version:1,course:'ai-engineering-16-weeks-v1',exportedAt:new Date().toISOString(),completed:[...steps].sort((a,b)=>a-b)}}
function persist(steps){try{localStorage.setItem(STORAGE_KEY,JSON.stringify(snapshot(steps)))}catch(e){throw Error('Браузер не дозволив зберегти прогрес. Перевірте налаштування сховища.')}storageWarning=''}
try{const saved=localStorage.getItem(STORAGE_KEY);if(saved!==null)completed=validateBackup(JSON.parse(saved))}catch(e){storageWarning='Не вдалося прочитати збережений прогрес. Експортуйте наявний файл або перевірте сховище браузера.';toast(storageWarning)}
function render(){const n=completed.size,p=Math.round(n/64*100);$('progressText').textContent=`${n} із 64 кроків`;$('percent').textContent=p+'%';$('bar').style.width=p+'%';$('progressHint').textContent=storageWarning||'Прогрес автоматично зберігається в цьому браузері.';$('modules').replaceChildren();topics.forEach((t,i)=>{const count=[0,1,2,3].filter(j=>completed.has(i*4+j)).length;if(filter==='done'&&count!==4||filter==='active'&&(count===0||count===4))return;const b=document.createElement('button');b.className='module';b.innerHTML=`<div class="moduleTop"><span>ТИЖДЕНЬ ${String(i+1).padStart(2,'0')}</span><span>${count===4?'✓ ЗАВЕРШЕНО':count?'У ПРОЦЕСІ':'↗'}</span></div><div class="moduleIcon">${['⌘','∑','✳','≋','↔','◈','▤','⤳'][i%8]}</div><h3>${t[0]}</h3><p>${t[1]}</p><div class="moduleBottom"><span>${count}/4 кроки виконано</span><span>Відкрити →</span></div>`;b.onclick=()=>lesson(i);$('modules').append(b)})}
function lesson(i){const t=topics[i];$('lessonContent').innerHTML=`<div class="eyebrow">ТИЖДЕНЬ ${i+1} · 4–6 ГОДИН</div><h2>${t[0]}</h2><p>${t[2]}</p><svg class="diagram" viewBox="0 0 720 125" role="img" aria-label="${t[7].join(' → ')}"><defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#6b8b5a"/></marker></defs>${t[7].map((label,j)=>`<rect x="${15+j*180}" y="35" width="150" height="55" rx="10" fill="${j===3?'#285a43':'#dfe9d6'}"/><text x="${90+j*180}" y="67" text-anchor="middle" fill="${j===3?'white':'#285a43'}" font-size="13" font-family="system-ui">${label}</text>${j<3?`<line x1="${168+j*180}" y1="62" x2="${191+j*180}" y2="62" stroke="#6b8b5a" stroke-width="2" marker-end="url(#arrow)"/>`:''}`).join('')}</svg><h3>Матеріали та відео</h3><p><a href="${t[5]}" target="_blank" rel="noopener">Читати безкоштовний матеріал ↗</a><br><a href="https://www.youtube.com/results?search_query=${encodeURIComponent(t[6])}" target="_blank" rel="noopener">Знайти відео на YouTube за темою ↗</a></p><p>Це тематичний пошук, а не перевірена добірка роликів. Більшість джерел англійською; пояснення й завдання українською.</p><h3>Практичне завдання</h3><p>${t[3]}</p><h3>Стартовий приклад</h3><p>Фрагмент демонструє підхід; залежності та решту проєкту потрібно підготувати в межах завдання.</p><pre><code id="snippet"></code></pre><h3>Критерій перевірки</h3><p id="criterion"></p><h3>Ваші кроки</h3><div id="tasks"></div>`;
// Tuple: title, subtitle, theory, practice, criterion, resource, video, diagram.
$('snippet').textContent=snippets[i];$('criterion').textContent=t[4];const labels=['Прочитано теорію й матеріали','Переглянуто відео або конспект за темою','Виконано практичне завдання','Перевірено всі критерії'];labels.forEach((label,j)=>{const row=document.createElement('label');row.className='task';const input=document.createElement('input');input.type='checkbox';input.checked=completed.has(i*4+j);input.onchange=()=>{const next=new Set(completed);input.checked?next.add(i*4+j):next.delete(i*4+j);try{persist(next);completed=next;render()}catch(e){input.checked=!input.checked;toast(e.message)}};row.append(input,document.createTextNode(label));$('tasks').append(row)});$('lessonDialog').showModal()}
$('continue').onclick=()=>lesson(topics.findIndex((_,i)=>[0,1,2,3].some(j=>!completed.has(i*4+j)))===-1?15:topics.findIndex((_,i)=>[0,1,2,3].some(j=>!completed.has(i*4+j))));
document.querySelectorAll('[data-filter]').forEach(b=>b.onclick=()=>{filter=b.dataset.filter;document.querySelectorAll('[data-filter]').forEach(x=>x.classList.toggle('selected',x===b));render()});
document.querySelectorAll('.close').forEach(b=>b.onclick=()=>b.closest('dialog').close());

function view(backup){$('courseView').hidden=backup;$('backupView').hidden=!backup;$('courseNav').classList.toggle('active',!backup);$('backupNav').classList.toggle('active',backup)}
$('courseNav').onclick=()=>view(false);
$('backupNav').onclick=$('backupButton').onclick=()=>view(true);
$('exportButton').onclick=()=>{
  const blob=new Blob([JSON.stringify(snapshot(completed),null,2)],{type:'application/json'});
  const url=URL.createObjectURL(blob),link=document.createElement('a');
  link.href=url;link.download='ai-atelier-progress-'+new Date().toISOString().slice(0,10)+'.json';
  document.body.append(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
  $('backupStatus').textContent='Резервну копію експортовано. Збережіть файл у надійному місці.';
};
$('importButton').onclick=async()=>{
  const file=$('importFile').files[0];
  try{
    if(!file)throw Error('Виберіть JSON-файл резервної копії.');
    if(file.size>100000)throw Error('Файл завеликий для резервної копії прогресу.');
    const imported=validateBackup(JSON.parse(await file.text()));
    const merged=new Set([...completed,...imported]);persist(merged);completed=merged;render();
    $('backupStatus').textContent=`Відновлено: ${completed.size} із 64 кроків. Поточний прогрес збережено.`;
    $('importFile').value='';
  }catch(e){$('backupStatus').textContent=e instanceof SyntaxError?'Файл не містить коректний JSON.':e.message}
};
window.addEventListener('storage',event=>{
  if(event.key!==STORAGE_KEY&&event.key!==null)return;
  try{completed=event.newValue?validateBackup(JSON.parse(event.newValue)):new Set();render();if($('lessonDialog').open)$('lessonDialog').close();toast('Прогрес оновлено в іншій вкладці.')}catch(e){toast('Не вдалося прочитати прогрес з іншої вкладки.')}
});
render();
