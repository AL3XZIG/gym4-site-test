(function(){
"use strict";
var form=document.getElementById("adminDemoForm");
if(!form)return;
var title=form.elements.title, body=form.elements.body, status=document.getElementById("adminDemoStatus"), saved=document.getElementById("adminDemoSaved"), previewTitle=document.getElementById("adminDemoPreviewTitle"), previewText=document.getElementById("adminDemoPreviewText"), reset=document.getElementById("adminDemoReset"), key="gym4-admin-demo-draft-v1";
var initial={title:title.value,body:body.value};
function render(){previewTitle.textContent=title.value.trim()||"Без заголовка";previewText.textContent=body.value.trim()||"Текст объявления не заполнен.";status.textContent="Есть несохранённые изменения";saved.textContent="Черновик изменён";}
[title,body].forEach(function(field){field.addEventListener("input",render);});
try{var draft=JSON.parse(localStorage.getItem(key)||"null");if(draft&&typeof draft.title==="string"&&typeof draft.body==="string"){title.value=draft.title;body.value=draft.body;previewTitle.textContent=draft.title||"Без заголовка";previewText.textContent=draft.body||"Текст объявления не заполнен.";status.textContent="Черновик загружен";saved.textContent="Черновик восстановлен из этого браузера";}}catch(error){}
form.addEventListener("submit",function(event){event.preventDefault();var draft={title:title.value.trim(),body:body.value.trim(),savedAt:new Date().toISOString()};try{localStorage.setItem(key,JSON.stringify(draft));status.textContent="Черновик сохранён";saved.textContent="Сохранено локально в этом браузере";}catch(error){status.textContent="Не удалось сохранить";saved.textContent="Хранилище браузера недоступно";}});
reset.addEventListener("click",function(){title.value=initial.title;body.value=initial.body;try{localStorage.removeItem(key);}catch(error){}previewTitle.textContent=initial.title;previewText.textContent=initial.body;status.textContent="Сброшено";saved.textContent="Черновик удалён из локального хранилища";});
})();
