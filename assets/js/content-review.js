(function(){
"use strict";
var KEY="gym4-content-review-v1";
var ITEMS=[
 ["identity","Реквизиты","Полное и краткое наименование","Сверить формулировки с уставом и учредительными документами."],
 ["founding","Реквизиты","Дата основания и история","Разделять дату основания школы и дату создания гимназии; приложить подтверждающий источник."],
 ["contacts","Контакты","Адрес и телефоны","Сверить адрес, телефоны, режим работы и график приёма с ответственным сотрудником."],
 ["email","Контакты","Официальные адреса электронной почты","На источнике встречаются разные e-mail. Подтвердить действующие адреса и удалить устаревшие."],
 ["leadership","Контакты","Руководство и приёмные часы","Подтвердить ФИО, должности, рабочие контакты и приёмные часы перед публикацией."],
 ["route","Контакты","Карта и доступная среда","Проверить адресную точку, входы, доступность помещений и актуальность маршрутной информации."],
 ["sveden-structure","Сведения","Структура и органы управления","Сверить подразделы, коллегиальные органы, положения и ответственных."],
 ["sveden-docs","Сведения","Устав, лицензия и локальные документы","Проверить оригиналы, даты, номера, подписи, ссылки и версии файлов."],
 ["sveden-education","Сведения","Образовательные программы и учебный график","Подтвердить уровни, формы, сроки обучения, учебные планы и календарный график текущего года."],
 ["sveden-staff","Сведения","Педагогический состав и руководство","Проверить должности, образование, квалификацию, преподаваемые дисциплины и основания публикации персональных сведений."],
 ["sveden-access","Сведения","Материальная база, питание и доступность","Подтвердить описание объектов, режим питания, специальные условия и актуальные сведения."],
 ["admission-dates","Приём","Сроки и порядок приёма","Обновить учебный год, сроки, способы подачи заявлений и действующие нормативные документы."],
 ["admission-area","Приём","Микроучасток и вакантные места","Сверить новое распоряжение о закреплённой территории и указать дату актуальности числа мест."],
 ["student-schedule","Обучающимся","Расписание, каникулы и звонки","Использовать только утверждённые расписания; проверить даты обновления и классные варианты."],
 ["school-life","Школьная жизнь","Календарь, достижения и кружки","Подтвердить мероприятия, результаты, названия объединений, возрастные группы и расписание."],
 ["news","Новости","Даты, источники и актуальность публикаций","Проверить первоисточник, дату, текст, категорию и срок действия объявлений."],
 ["media-rights","Медиа","Фотографии, видео и подписи","Получить разрешения на публикацию материалов и проверить отсутствие лишних персональных данных обучающихся."],
 ["partners","Партнёры","Список партнёров и внешние ссылки","Добавлять только согласованные организации и проверенные URL."],
 ["a11y","Доступность","Клавиатура, контраст и масштабирование","Проверить фокус, порядок табуляции, контраст, масштаб 200%, мобильную компоновку и экранный диктор."],
 ["privacy","Безопасность","Формы, персональные данные и доступы","Не включать сбор обращений до утверждения процесса обработки данных и защищённого серверного механизма."],
 ["release","Публикация","Проверка ссылок и сборки","Запустить tools/check_site.py и GitHub Actions; отдельно проверить ссылки, документы и страницы на мобильном устройстве."]
];
var LABELS={todo:"Не проверено",ok:"Подтверждено",fix:"Требует исправления"};
var dialog=document.getElementById("contentReviewDialog"),list=document.getElementById("reviewItemList");
if(!dialog||!list)return;
var state={},filter="all";
function load(){
 try{var saved=JSON.parse(localStorage.getItem(KEY)||"{}");ITEMS.forEach(function(x){var v=saved[x[0]];state[x[0]]=v==="ok"||v==="fix"?v:"todo";});}
 catch(e){ITEMS.forEach(function(x){state[x[0]]="todo";});}
}
function save(){
 try{localStorage.setItem(KEY,JSON.stringify(state));}
 catch(e){var note=document.getElementById("reviewStorageNote");if(note)note.textContent="Браузер не разрешил сохранить отметки. Экспортируйте отчёт перед закрытием.";}
}
function updateProgress(){
 var done=ITEMS.filter(function(x){return state[x[0]]==="ok";}).length,fix=ITEMS.filter(function(x){return state[x[0]]==="fix";}).length;
 var p=document.getElementById("reviewProgress");p.max=ITEMS.length;p.value=done;
 document.getElementById("reviewProgressLabel").textContent="Подтверждено: "+done+" из "+ITEMS.length;
 document.getElementById("reviewStatusLabel").textContent=fix?fix+" пунктов требуют исправления":(done===ITEMS.length?"Все пункты подтверждены":"Осталось проверить: "+(ITEMS.length-done));
}
function render(){
 list.textContent="";
 var shown=ITEMS.filter(function(x){return filter==="all"||state[x[0]]===filter;});
 if(!shown.length){var empty=document.createElement("p");empty.className="review-empty";empty.textContent="В этой категории пока нет пунктов.";list.appendChild(empty);}
 var last="";
 shown.forEach(function(item){
  if(last!==item[1]){last=item[1];var heading=document.createElement("h3");heading.className="review-group-title";heading.textContent=last;list.appendChild(heading);}
  var card=document.createElement("article"),text=document.createElement("div"),title=document.createElement("strong"),description=document.createElement("p"),control=document.createElement("div"),label=document.createElement("label"),select=document.createElement("select");
  card.className="review-item";card.dataset.status=state[item[0]];
  title.textContent=item[2];description.textContent=item[3];text.append(title,description);
  label.textContent="Статус проверки";label.htmlFor="review-"+item[0];select.id="review-"+item[0];select.setAttribute("aria-label","Статус: "+item[2]);
  Object.keys(LABELS).forEach(function(k){var option=document.createElement("option");option.value=k;option.textContent=LABELS[k];select.appendChild(option);});
  select.value=state[item[0]];
  select.addEventListener("change",function(){state[item[0]]=select.value;save();card.dataset.status=select.value;card.hidden=filter!=="all"&&filter!==select.value;updateProgress();});
  control.append(label,select);card.append(text,control);list.appendChild(card);
 });
 document.querySelectorAll("[data-review-filter]").forEach(function(b){b.setAttribute("aria-pressed",String(b.dataset.reviewFilter===filter));});
 updateProgress();
}
function open(){if(typeof dialog.showModal==="function")dialog.showModal();else dialog.setAttribute("open","");}
function close(){if(typeof dialog.close==="function"&&dialog.open)dialog.close();else dialog.removeAttribute("open");}
function exportReport(){
 var done=ITEMS.filter(function(x){return state[x[0]]==="ok";}).length,fix=ITEMS.filter(function(x){return state[x[0]]==="fix";}).length;
 var lines=["# Контроль готовности сайта Гимназии № 4","","Дата выгрузки: "+new Date().toLocaleString("ru-RU"),"","Подтверждено: "+done+" из "+ITEMS.length,"Требует исправления: "+fix,"","Отметки — локальная самооценка. Они не являются официальным подтверждением администрации.",""];
 var group="";
 ITEMS.forEach(function(x){if(group!==x[1]){group=x[1];lines.push("## "+group,"");}lines.push("- ["+(state[x[0]]==="ok"?"x":" ")+"] **"+x[2]+"** — "+LABELS[state[x[0]]]+". "+x[3]);});
 lines.push("","---","Отчёт сформирован демонстрационным инструментом в браузере. Для официальной приёмки приложите первоисточники и согласование ответственных сотрудников.");
 var blob=new Blob([lines.join("\n")],{type:"text/markdown;charset=utf-8"}),url=URL.createObjectURL(blob),a=document.createElement("a");
 a.href=url;a.download="gym4-content-readiness-"+new Date().toISOString().slice(0,10)+".md";document.body.appendChild(a);a.click();a.remove();window.setTimeout(function(){URL.revokeObjectURL(url);},1000);
}
document.getElementById("openReviewBtn").addEventListener("click",open);
document.getElementById("closeReviewBtn").addEventListener("click",close);
document.getElementById("exportReviewBtn").addEventListener("click",exportReport);
document.getElementById("resetReviewBtn").addEventListener("click",function(){if(!window.confirm("Сбросить все локальные отметки проверки?"))return;ITEMS.forEach(function(x){state[x[0]]="todo";});save();render();});
document.querySelectorAll("[data-review-filter]").forEach(function(b){b.addEventListener("click",function(){filter=b.dataset.reviewFilter;render();});});
dialog.addEventListener("click",function(e){if(e.target===dialog)close();});
load();render();
})();