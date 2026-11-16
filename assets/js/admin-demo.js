(function(){
"use strict";
var $=function(id){return document.getElementById(id);};
var frame=$("siteFrame"), page=$("pageSelect"), status=$("editorStatus"), form=$("elementForm");
var textField=$("elementText"), imageFields=$("imageFields"), linkFields=$("linkFields");
var imageUrl=$("imageUrl"), imageAlt=$("imageAlt"), linkUrl=$("linkUrl");
var current=null, currentDoc=null, history=[], future=[], editMode=true, draftKey="gym4-site-editor-v2", pageName=page.options[page.selectedIndex].text;
function say(message){status.textContent=message;}
function snapshot(){if(!currentDoc)return;history.push(frame.contentDocument.documentElement.outerHTML);if(history.length>40)history.shift();future=[];buttons();}
function buttons(){$("undoBtn").disabled=!history.length;$("redoBtn").disabled=!future.length;}
function restore(html){var doc=frame.contentDocument;doc.open();doc.write(html);doc.close();attachEditor();current=null;showEmpty();buttons();}
function showEmpty(){ $("emptyInspector").hidden=false;form.hidden=true;$("selectionInfo").textContent="Элемент не выбран";$("inspectorDescription").textContent="Выберите текст, изображение или ссылку в макете."; }
function label(el){return el.tagName.toLowerCase()+(el.id?"#"+el.id:"")+(el.classList&&el.classList.length?"."+Array.from(el.classList).slice(0,2).join("."):"");}
function clearMarks(){if(!current)return;current.style.outline="";current.removeAttribute("data-editor-selected");}
function selectElement(el){
 if(!el||/^(HTML|BODY|SCRIPT|STYLE|LINK|META|HEAD|NAV|HEADER|FOOTER)$/.test(el.tagName))return;
 clearMarks();current=el;el.setAttribute("data-editor-selected","true");el.style.outline="2px solid #bd8b3b";
 $("emptyInspector").hidden=true;form.hidden=false;
 var isImg=el.tagName==="IMG", isLink=el.tagName==="A";
 textField.value=isImg?(el.getAttribute("alt")||""):(el.innerText||el.textContent||"").trim();
 imageFields.hidden=!isImg;linkFields.hidden=!isLink;
 if(isImg){imageUrl.value=el.getAttribute("src")||"";imageAlt.value=el.getAttribute("alt")||"";}
 if(isLink)linkUrl.value=el.getAttribute("href")||"";
 $("selectionInfo").textContent="Выбрано: "+label(el);$("inspectorDescription").textContent="Тег "+el.tagName.toLowerCase()+" · изменения применяются к предпросмотру.";
}
function attachEditor(){
 currentDoc=frame.contentDocument;if(!currentDoc)return;
 currentDoc.addEventListener("click",function(e){
  if(!editMode)return;
  var el=e.target.closest("img,a,h1,h2,h3,h4,p,li,button,figcaption,blockquote,td,th,span,strong");
  if(!el)return;
  e.preventDefault();e.stopPropagation();selectElement(el);
 },true);
 currentDoc.addEventListener("mouseover",function(e){if(!editMode)return;var el=e.target.closest("img,a,h1,h2,h3,h4,p,li,button,figcaption,blockquote,td,th,span,strong");if(el&&!el.hasAttribute("data-editor-selected"))el.style.cursor="crosshair";},true);
 currentDoc.addEventListener("keydown",function(e){if(e.key==="Escape"){clearMarks();current=null;showEmpty();}});
 $("canvasHint").textContent="Нажмите на элемент, который хотите изменить";
 say("Страница загружена");
}
frame.addEventListener("load",function(){attachEditor();});
function loadPage(value,fromDraft){
 pageName=page.options[page.selectedIndex].text;$("currentPageName").textContent=pageName;
 current=null;showEmpty();history=[];future=[];buttons();
 frame.src=value;
}
page.addEventListener("change",function(){loadPage(page.value,false);});
$("editModeBtn").addEventListener("click",function(){editMode=!editMode;this.classList.toggle("is-active",editMode);this.textContent=editMode?"↖ Режим выбора":"⏸ Выбор отключён";$("canvasHint").textContent=editMode?"Нажмите на элемент, который хотите изменить":"Режим выбора отключён";});
form.addEventListener("submit",function(e){
 e.preventDefault();if(!current)return;snapshot();
 if(current.tagName==="IMG"){current.setAttribute("src",imageUrl.value.trim());current.setAttribute("alt",imageAlt.value.trim());}
 else current.textContent=textField.value;
 if(current.tagName==="A")current.setAttribute("href",linkUrl.value.trim());
 current.style.outline="2px solid #bd8b3b";say("Изменение применено · не сохранено");selectElement(current);
});
$("undoBtn").addEventListener("click",function(){if(!history.length)return;future.push(frame.contentDocument.documentElement.outerHTML);restore(history.pop());say("Действие отменено");});
$("redoBtn").addEventListener("click",function(){if(!future.length)return;history.push(frame.contentDocument.documentElement.outerHTML);restore(future.pop());say("Действие восстановлено");});
$("reloadBtn").addEventListener("click",function(){if(confirm("Перезагрузить страницу и потерять несохранённые изменения?"))loadPage(page.value,false);});
$("clearSelectionBtn").addEventListener("click",function(){clearMarks();current=null;showEmpty();});
function cleanHTML(){var doc=frame.contentDocument;var clone=doc.documentElement.cloneNode(true);clone.querySelectorAll("[data-editor-selected]").forEach(function(el){el.removeAttribute("data-editor-selected");el.style.outline="";});clone.querySelectorAll("[contenteditable]").forEach(function(el){el.removeAttribute("contenteditable");});return "<!doctype html>\n"+clone.outerHTML;}
$("saveDraftBtn").addEventListener("click",function(){
 try{var all={};try{all=JSON.parse(localStorage.getItem(draftKey)||"{}");}catch(e){}
 all[page.value]={html:cleanHTML(),savedAt:new Date().toISOString()};localStorage.setItem(draftKey,JSON.stringify(all));say("Черновик сохранён локально");}
 catch(e){say("Ошибка сохранения: хранилище недоступно");}
});
$("exportBtn").addEventListener("click",function(){
 var html=cleanHTML(),blob=new Blob([html],{type:"text/html;charset=utf-8"}),url=URL.createObjectURL(blob),a=document.createElement("a");
 a.href=url;a.download=page.value.split("/").pop()||"page.html";document.body.appendChild(a);a.click();a.remove();URL.revokeObjectURL(url);say("HTML экспортирован · проверьте файл перед заменой на сервере");
});
try{
 var all=JSON.parse(localStorage.getItem(draftKey)||"{}"),saved=all[page.value];
 if(saved&&saved.html&&confirm("Найден локальный черновик для этой страницы. Загрузить его?")){
  frame.addEventListener("load",function once(){frame.removeEventListener("load",once);restore(saved.html);say("Черновик восстановлен");});
 }
}catch(e){}
loadPage(page.value,true);
})();