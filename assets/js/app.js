(() => {
"use strict";
const $=(s,c=document)=>c.querySelector(s), $$=(s,c=document)=>[...c.querySelectorAll(s)];
const store={get(k,d){try{return JSON.parse(localStorage.getItem(k))??d}catch{return d}},set(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch{}}};
const root=document.documentElement;
const toastEl=$("#toast"),toastText=$("#toastText"),toastAction=$("#toastAction");
let toastTimer,actionFn=null;
const toast=(msg,actionLabel,fn)=>{if(!toastEl)return;toastText.textContent=msg;actionFn=fn||null;toastAction.hidden=!actionLabel;toastAction.textContent=actionLabel||"";toastEl.classList.add("show");clearTimeout(toastTimer);toastTimer=setTimeout(()=>toastEl.classList.remove("show"),actionLabel?6000:2600)};
if(toastAction)toastAction.onclick=()=>{if(actionFn)actionFn();toastEl.classList.remove("show")};
const year=$("#year");if(year)year.textContent=new Date().getFullYear();

/* scroll: progress, header, parallax */
const header=$("#siteHeader"),toTop=$("#toTop"),parallax=$$("[data-parallax]");
let ticking=false;
const onScroll=()=>{if(ticking)return;ticking=true;requestAnimationFrame(()=>{
 const max=root.scrollHeight-innerHeight;root.style.setProperty("--scroll",max>0?(scrollY/max).toFixed(4):0);
 if(header)header.classList.toggle("scrolled",scrollY>8);
 if(toTop)toTop.classList.toggle("show",scrollY>650);
 if(!root.classList.contains("no-motion"))parallax.forEach(el=>{const sp=+el.dataset.parallax||.12;el.style.transform="translateY("+Math.min(scrollY,700)*sp+"px)"});
 ticking=false})};
addEventListener("scroll",onScroll,{passive:true});onScroll();
if(toTop)toTop.onclick=()=>scrollTo({top:0,behavior:root.classList.contains("no-motion")?"auto":"smooth"});

/* mobile menu */
const burger=$("#burger"),nav=$("#nav");
const setMenu=o=>{if(!burger||!nav)return;nav.classList.toggle("open",o);burger.setAttribute("aria-expanded",String(o));burger.setAttribute("aria-label",o?"Закрыть меню":"Открыть меню");burger.textContent=o?"✕":"☰"};
if(burger)burger.onclick=()=>setMenu(!nav.classList.contains("open"));
if(nav)nav.addEventListener("click",e=>{if(e.target.closest("a"))setMenu(false)});

/* accessibility */
const panel=$("#a11yPanel"),aBtn=$("#a11yBtn"),fsRange=$("#fsRange"),fsValue=$("#fsValue"),motion=$("#motionToggle"),schemes=$$(".scheme");
let a11y=Object.assign({fs:100,scheme:"",motion:true},store.get("gym4-a11y",{}));
const applyA11y=s=>{root.style.fontSize=s.fs+"%";document.body.dataset.scheme=s.scheme||"";root.classList.toggle("no-motion",!s.motion||matchMedia("(prefers-reduced-motion: reduce)").matches);if(fsRange)fsRange.value=s.fs;if(fsValue)fsValue.textContent=s.fs+"%";if(motion)motion.checked=!!s.motion;schemes.forEach(b=>b.classList.toggle("on",(b.dataset.scheme||"")===(s.scheme||"")))};
applyA11y(a11y);
const setPanel=o=>{if(!panel||!aBtn)return;panel.hidden=!o;aBtn.setAttribute("aria-expanded",String(o))};
if(aBtn)aBtn.onclick=()=>setPanel(panel.hidden);
if($("#a11yClose"))$("#a11yClose").onclick=()=>setPanel(false);
if(fsRange)fsRange.oninput=()=>{a11y.fs=+fsRange.value;applyA11y(a11y);store.set("gym4-a11y",a11y)};
schemes.forEach(b=>b.onclick=()=>{a11y.scheme=b.dataset.scheme||"";applyA11y(a11y);store.set("gym4-a11y",a11y)});
if(motion)motion.onchange=()=>{a11y.motion=motion.checked;applyA11y(a11y);store.set("gym4-a11y",a11y)};
if($("#a11yReset"))$("#a11yReset").onclick=()=>{a11y={fs:100,scheme:"",motion:true};applyA11y(a11y);store.set("gym4-a11y",a11y);toast("Обычная версия восстановлена")};
addEventListener("keydown",e=>{if(e.key==="Escape"){setMenu(false);setPanel(false)}});

/* cookie */
const cookie=$("#cookie");
if(cookie&&!store.get("gym4-cookie",false))cookie.hidden=false;
if($("#cookieOk"))$("#cookieOk").onclick=()=>{store.set("gym4-cookie",true);cookie.hidden=true;toast("Настройки сохранены")};

/* reveals + count-up + mood */
const noMotion=()=>root.classList.contains("no-motion");
const targets=$$(".hero .container > *, main h2, main .card, .page-hero .container > *, .timeline li");
if("IntersectionObserver" in window){
 const io=new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting){en.target.classList.add("in");io.unobserve(en.target)}}),{threshold:.12});
 targets.forEach((el,i)=>{el.classList.add("rv");el.style.transitionDelay=(i%5)*55+"ms";io.observe(el)});
 const cio=new IntersectionObserver(es=>es.forEach(en=>{if(!en.isIntersecting)return;const el=en.target;cio.unobserve(el);const end=+el.dataset.count,suf=el.dataset.suffix||"";if(noMotion()){el.textContent=end+suf;return}
  const t0=performance.now(),dur=1200;const step=t=>{const p=Math.min((t-t0)/dur,1),e=1-Math.pow(1-p,3);el.textContent=Math.round(end*e)+suf;if(p<1)requestAnimationFrame(step)};requestAnimationFrame(step)}),{threshold:.5});
 $$("[data-count]").forEach(el=>cio.observe(el));
 const moods={gold:"0deg",blue:"38deg",green:"86deg",red:"-28deg"};
 const mio=new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting)root.style.setProperty("--amb",moods[en.target.dataset.mood]||"0deg")}),{threshold:.35});
 $$("[data-mood]").forEach(el=>mio.observe(el));
}else{targets.forEach(el=>el.classList.add("in"));$$("[data-count]").forEach(el=>el.textContent=el.dataset.count+(el.dataset.suffix||""))}

/* scrollspy for aside */
const aside=$(".aside-nav");
if(aside&&"IntersectionObserver" in window){
 const links=$$("a[href^='#']",aside),map=new Map(links.map(a=>[a.getAttribute("href").slice(1),a]));
 const sio=new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting){links.forEach(a=>a.classList.remove("on"));const a=map.get(en.target.id);if(a)a.classList.add("on")}}),{rootMargin:"-30% 0px -60% 0px"});
 map.forEach((a,id)=>{const sec=document.getElementById(id);if(sec)sio.observe(sec)});
}

/* news: search + filter + sort */
const list=$("#newsList");
if(list){
 const search=$("#newsSearch"),sort=$("#newsSort"),count=$("#newsCount"),empty=$("#newsEmpty");
 let cat="all";
 const items=$$("#newsList [data-cat]");
 const apply=()=>{const q=(search?.value||"").trim().toLowerCase();
  const sorted=[...items].sort((a,b)=>sort.value==="asc"?a.dataset.date.localeCompare(b.dataset.date):b.dataset.date.localeCompare(a.dataset.date));
  sorted.forEach(el=>list.appendChild(el));let n=0;
  items.forEach(el=>{const ok=(cat==="all"||el.dataset.cat===cat)&&(!q||el.textContent.toLowerCase().includes(q));el.hidden=!ok;if(ok)n++});
  count.textContent="Показано: "+n+" из "+items.length;empty.hidden=n!==0};
 $$("[data-filter]").forEach(b=>b.onclick=()=>{cat=b.dataset.filter;if(!b.closest(".filter")&&search)search.value="";$$(".filter button").forEach(x=>x.classList.toggle("on",x.dataset.filter===cat));apply()});
 if(search)search.oninput=apply;if(sort)sort.onchange=apply;apply();
}

/* Demo form: never transmits or persists user input. */
const form=$("#fbForm");
if(form)form.addEventListener("submit",e=>{e.preventDefault();toast("Демо-режим: данные не отправлены и не сохранены.")});

/* copy hex */
const copy=async t=>{try{await navigator.clipboard.writeText(t)}catch{const ta=document.createElement("textarea");ta.value=t;ta.style.position="fixed";ta.style.opacity="0";document.body.appendChild(ta);ta.select();document.execCommand("copy");ta.remove()}toast("Скопировано: "+t)};
$$("[data-copy]").forEach(b=>b.onclick=()=>copy(b.dataset.copy));
})();
'''