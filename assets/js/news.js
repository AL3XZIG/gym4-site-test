(function(){
"use strict";
var list=document.getElementById("newsList");if(!list)return;
var search=document.getElementById("newsSearch"),sort=document.getElementById("newsSort"),count=document.getElementById("newsCount"),empty=document.getElementById("newsEmpty"),buttons=[].slice.call(document.querySelectorAll("[data-filter]")),active="all",posts=[],seasonalPosts=[];
function safeHttpUrl(value){try{var u=new URL(value,window.location.href);return (u.protocol==="http:"||u.protocol==="https:")?u.href:""}catch(e){return ""}}
function safeImageUrl(value){var v=String(value||"").trim();if(!v||v.startsWith("//"))return "";if(/^https:\/\//i.test(v))return safeHttpUrl(v);if(!/^\/?assets\/[a-z0-9_./-]+$/i.test(v)&&!/^\/media\/[a-z0-9_./-]+$/i.test(v))return "";if(v.split("/").some(function(part){return part==="..";}))return "";return v}
function currentTheme(){return document.documentElement.getAttribute("data-season-theme")||"autumn";}
function render(){
 var q=search?search.value.trim().toLocaleLowerCase("ru"):"",theme=currentTheme();
 var visiblePosts=posts.filter(function(p){return !p.season||p.season===theme;});
 var ordered=visiblePosts.slice().sort(function(a,b){return sort&&sort.value==="asc"?a.date.localeCompare(b.date):b.date.localeCompare(a.date)}),shown=0;
 list.textContent="";
 ordered.forEach(function(p){
  var hay=(p.title+" "+p.excerpt+" "+(p.body||"")).toLocaleLowerCase("ru");
  if((active!=="all"&&p.category!==active)||(q&&hay.indexOf(q)<0))return;
  shown++;var article=document.createElement("article");article.className="news-entry"+(p.season?" news-entry--seasonal":"");article.dataset.cat=p.category;article.dataset.date=p.date;
  var time=document.createElement("time");time.className="news-entry__date";time.dateTime=p.date;time.textContent=new Date(p.date+"T12:00:00").toLocaleDateString("ru-RU")+" · "+({news:"Новости",events:"Мероприятие",announcements:"Объявление"}[p.category]||"Новости");
  var h=document.createElement("h3"),source=safeHttpUrl(p.sourceUrl||"");
  if(source){var a=document.createElement("a");a.textContent=p.title||"Без заголовка";a.href=source;a.target="_blank";a.rel="noopener noreferrer";h.appendChild(a);}
  else h.textContent=p.title||"Без заголовка";
  var imageUrl=safeImageUrl(p.imageUrl);if(imageUrl){var image=document.createElement("img");image.className="news-entry__image";image.src=imageUrl;image.alt=p.title||"Иллюстрация к публикации";image.loading="lazy";image.decoding="async";article.appendChild(image);}
  if(p.season){var badge=document.createElement("span");badge.className="news-entry__demo-label";badge.textContent="СЕЗОННАЯ ДЕМО-НОВОСТЬ · "+({winter:"ЗИМА",spring:"ВЕСНА",summer:"ЛЕТО",autumn:"ОСЕНЬ"}[p.season]||"ДЕМО");article.appendChild(badge);}
  var para=document.createElement("p");para.textContent=p.excerpt||p.body||"";
  article.append(time,h,para);
  if(source){var meta=document.createElement("span");meta.className="news-entry__meta";meta.textContent="Источник: "+(p.sourceName||"внешняя публикация");article.appendChild(meta);}
  list.appendChild(article);
 });
 if(count)count.textContent=shown?"Показано публикаций: "+shown:"Публикаций по заданным условиям не найдено.";
 if(empty)empty.hidden=shown!==0;
}
function mergePosts(live,statik,seasonal){
 var merged=Array.isArray(live.posts)?live.posts.slice():[],ids=new Set(merged.map(function(p){return String(p.id)}));
 (Array.isArray(statik.posts)?statik.posts:[]).forEach(function(p){if(!ids.has(String(p.id))){merged.push(p);ids.add(String(p.id));}});
 (Array.isArray(seasonal.posts)?seasonal.posts:[]).forEach(function(p){if(!ids.has(String(p.id))){merged.push(p);ids.add(String(p.id));}});
 posts=merged;render();
}
Promise.all([
 fetch("/api/v1/public/news/").then(function(r){if(!r.ok)throw Error("live news unavailable");return r.json();}).catch(function(){return {posts:[]};}),
 fetch("assets/data/news.json").then(function(r){if(!r.ok)throw Error("static news unavailable");return r.json();}).catch(function(){return {posts:[]};}),
 fetch("assets/data/seasonal-news.json").then(function(r){if(!r.ok)throw Error("seasonal news unavailable");return r.json();}).catch(function(){return {posts:[]};})
]).then(function(data){mergePosts(data[0],data[1],data[2]);}).catch(function(){posts=[];render();});
buttons.forEach(function(b){b.addEventListener("click",function(){active=b.dataset.filter;buttons.forEach(function(x){var on=x===b;x.classList.toggle("is-active",on);x.setAttribute("aria-pressed",String(on));});render();});});
if(search)search.addEventListener("input",render);if(sort)sort.addEventListener("change",render);
document.addEventListener("gym4:seasonchange",render);
})();
