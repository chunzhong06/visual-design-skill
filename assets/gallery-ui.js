// 共享目录的离线预览；只筛选已登记本地文件，不联网、不自动选画风。
(() => {
  'use strict';
  const data=window.VISUAL_ASSET_LIBRARY;
  const $=id=>document.getElementById(id);
  const esc=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const norm=value=>String(value??'').normalize('NFKC').toLocaleLowerCase().replace(/[-_\s]+/g,' ').trim();
  const labels={icon:'图标','scientific-object':'科学图形',background:'背景',decoration:'装饰','diagram-part':'结构组件','layout-guide':'构图参考'};
  const familyLabels={lucide:'Lucide · 线性','phosphor-duotone':'Phosphor · 双色',original:'原创示意',opentikz:'OpenTikZ'};
  const params=new URLSearchParams(location.search);
  const state={module:params.get('module')||document.body.dataset.module||'',kind:params.get('kind')||'',family:params.get('family')||'',use:params.get('use')||'',tone:params.get('tone')||'',query:'',page:0};
  const prefix=document.body.dataset.prefix||'';
  const pageSize=48;
  const kinds=['',...Object.keys(labels)];
  $('kinds').innerHTML=kinds.map(k=>'<button type="button" data-kind="'+k+'" aria-pressed="false">'+(labels[k]||'全部')+'</button>').join('');
  $('family').innerHTML='<option value="">全部图形家族</option>'+[...new Set(data.assets.map(x=>x.family))].sort().map(f=>'<option value="'+esc(f)+'">'+esc(familyLabels[f]||f)+'</option>').join('');
  function matching(){
    const terms=norm(state.query).split(' ').filter(Boolean);
    return data.assets.filter(a=>(!state.module||a.modules.includes(state.module))&&(!state.kind||a.kind===state.kind)&&(!state.family||a.family===state.family)&&(!state.use||a.uses.includes(state.use))&&(!state.tone||a.tone===state.tone)&&terms.every(t=>a.search.includes(t)));
  }
  function sourceLink(a){return a.source_url?'<a href="'+esc(a.source_url)+'" target="_blank" rel="noopener noreferrer">来源</a>':'原创';}
  function card(a){
    const url=prefix+a.url;
    return '<article class="card" data-kind="'+esc(a.kind)+'"><h2>'+esc(a.name)+'</h2><div class="family">'+esc(familyLabels[a.family]||a.family)+' · '+esc(a.slug)+'</div><a class="thumb" href="'+esc(url)+'" target="_blank"><img src="'+esc(url)+'" loading="lazy" alt="'+esc(a.name)+'"></a><div class="tags"><span class="tag">'+esc(labels[a.kind])+'</span>'+(a.tone?'<span class="tag">'+(a.tone==='dark'?'深色':'浅色')+'</span>':'')+'</div>'+(a.meaning?'<p class="meaning">'+esc(a.meaning)+'</p>':'')+'<details><summary>用途与来源</summary><p class="meaning">'+esc(a.note||'按当前内容采用，语义和颜色以材料为准。')+'</p><p class="license">'+sourceLink(a)+' · '+esc(a.license)+'</p></details><div class="links"><a href="'+esc(url)+'" target="_blank">打开 SVG</a><a href="'+esc(url)+'" download>下载</a></div></article>';
  }
  function render(){
    for(const id of ['module','family','use','tone'])$(id).value=state[id];
    document.querySelectorAll('#kinds button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.kind===state.kind)));
    const matches=matching(),pages=Math.max(1,Math.ceil(matches.length/pageSize));
    state.page=Math.min(state.page,pages-1);
    const slice=matches.slice(state.page*pageSize,(state.page+1)*pageSize);
    $('cards').innerHTML=slice.map(card).join('');
    $('empty').hidden=matches.length>0;
    $('status').textContent='匹配 '+matches.length+' 项 · 实际本地文件共 '+data.stats.unique_local_files+' 个，跨目录按文件去重。';
    $('page').textContent=(state.page+1)+' / '+pages;
    $('prev').disabled=state.page===0;$('next').disabled=state.page>=pages-1;
  }
  $('query').addEventListener('input',()=>{state.query=$('query').value;state.page=0;render();});
  for(const id of ['module','family','use','tone'])$(id).addEventListener('change',()=>{state[id]=$(id).value;state.page=0;render();});
  $('kinds').addEventListener('click',event=>{const b=event.target.closest('button');if(!b)return;state.kind=b.dataset.kind;state.page=0;render();});
  $('reset').onclick=()=>{Object.assign(state,{module:'',kind:'',family:'',use:'',tone:'',query:'',page:0});$('query').value='';render();};
  $('prev').onclick=()=>{state.page--;render();$('status').scrollIntoView({block:'start'});};
  $('next').onclick=()=>{state.page++;render();$('status').scrollIntoView({block:'start'});};
  $('dark').onclick=()=>{const active=document.body.classList.toggle('dark-check');$('dark').setAttribute('aria-pressed',String(active));};
  document.querySelectorAll('[data-preset]').forEach(b=>b.onclick=()=>{
    const preset=b.dataset.preset;
    Object.assign(state,{module:'',kind:'',family:'',use:'',tone:'',query:'',page:0});$('query').value='';
    if(preset==='science'){state.module='research';state.kind='scientific-object';}
    if(preset==='paper'){state.module='research';state.kind='background';state.use='figure-panel';}
    if(preset==='ppt'){state.module='presentation';state.kind='background';state.use='slide-background';}
    if(preset==='structure')state.kind='diagram-part';
    render();
  });
  render();
})();
