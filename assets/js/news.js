(function(){
"use strict";
var list=document.getElementById("newsList");if(!list)return;
var search=document.getElementById("newsSearch"),sort=document.getElementById("newsSort"),count=document.getElementById("newsCount"),empty=document.getElementById("newsEmpty"),buttons=[].slice.call(document.querySelectorAll("[data-filter]")),active="all",posts=[];
function safeHttpUrl(value){try{var u=new URL(value,window.location.href);return (u.protocol==="http:"||u.protocol==="https:")?u.href:""}catch(e){return ""}}
function safeImageUrl(value){var v=String(value||"").trim();if(!v||v.startsWith("//"))return "";if(/^https:\/\//i.test(v))return safeHttpUrl(v);if(/^\/?assets\/[a-z0-9_./-]+$/i.test(v))return v;return ""}
function render(){
 var q=search?search.value.trim().toLocaleLowerCase("ru"):"",ordered=posts.slice().sort(function(a,b){return sort&&sort.value==="asc"?a.date.localeCompare(b.date):b.date.localeCompare(a.date)}),shown=0;
 list.textContent="";
 ordered.forEach(function(p){
  var hay=(p.title+" "+p.excerpt+" "+(p.body||"")).toLocaleLowerCase("ru");
  if((active!=="all"&&p.category!==active)||(q&&hay.indexOf(q)<0))return;
  shown++;var article=document.createElement("article");article.className="news-entry";article.dataset.cat=p.category;article.dataset.date=p.date;
  var time=document.createElement("time");time.className="news-entry__date";time.dateTime=p.date;time.textContent=new Date(p.date+"T12:00:00").toLocaleDateString("ru-RU")+" · "+({news:"Новости",events:"Мероприятие",announcements:"Объявление"}[p.category]||"Новости");
  var h=document.createElement("h3"),source=safeHttpUrl(p.sourceUrl||"");
  if(source){var a=document.createElement("a");a.textContent=p.title||"Без заголовка";a.href=source;a.target="_blank";a.rel="noopener noreferrer";h.appendChild(a);}
  else h.textContent=p.title||"Без заголовка";
  var imageUrl=safeImageUrl(p.imageUrl);if(imageUrl){var image=document.createElement("img");image.className="news-entry__image";image.src=imageUrl;image.alt=p.title||"Иллюстрация к публикации";image.loading="lazy";image.decoding="async";article.appendChild(image)}
  var para=document.createElement("p");para.textContent=p.excerpt||p.body||"";
  article.append(time,h,para);
  if(source){var meta=document.createElement("span");meta.className="news-entry__meta";meta.textContent="Источник: "+(p.sourceName||"внешняя публикация");article.appendChild(meta)}
  list.appendChild(article);
 });
 if(count)count.textContent=shown?"Показано публикаций: "+shown:"Публикаций по заданным условиям не найдено.";
 if(empty)empty.hidden=shown!==0;
}
fetch("assets/data/news.json").then(function(r){if(!r.ok)throw Error("news");return r.json()}).then(function(d){posts=Array.isArray(d.posts)?d.posts:[];render()}).catch(function(){posts=[];render()});
buttons.forEach(function(b){b.addEventListener("click",function(){active=b.dataset.filter;buttons.forEach(function(x){var on=x===b;x.classList.toggle("is-active",on);x.setAttribute("aria-pressed",String(on))});render()})});
if(search)search.addEventListener("input",render);if(sort)sort.addEventListener("change",render);
})();