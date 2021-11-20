(this["webpackJsonpnn-hn"]=this["webpackJsonpnn-hn"]||[]).push([[0],{102:function(e,n,t){},103:function(e,n,t){},112:function(e,n,t){"use strict";t.r(n);var r=t(0),a=t.n(r),c=t(27),o=t.n(c),i=(t(102),t(103),t(21)),s=t(4),l=t(161),d=t(165),u=t(14),b=t(29),j=Object(b.c)({name:"navigation",initialState:{page:"check"},reducers:{setPage:function(e,n){e.page=n.payload}}}),p=j.actions.setPage,f=function(e){return e.navigation.page},g=j.reducer,h=t(2),x=Object(s.a)((function(e){return Object(h.jsx)(d.a,Object(i.a)({disableRipple:!0},e))}))((function(e){var n=e.theme;return{textTransform:"none",fontWeight:n.typography.fontWeightRegular,fontSize:n.typography.pxToRem(15),marginRight:n.spacing(1),color:"rgba(0, 0, 0, 0.3)","&.Mui-selected":{color:"#000000"},"&.Mui-focusVisible":{backgroundColor:"rgba(255, 255, 255, 0.32)"}}})),O=Object(s.a)((function(e){return Object(h.jsx)(l.a,Object(i.a)(Object(i.a)({},e),{},{TabIndicatorProps:{children:Object(h.jsx)("span",{className:"MuiTabs-indicatorSpan"})}}))}))({"& .MuiTabs-indicator":{display:"flex",justifyContent:"center",backgroundColor:"transparent"},"& .MuiTabs-indicatorSpan":{maxWidth:40,width:"100%",backgroundColor:"#fff"}});function m(){var e=Object(u.b)(),n=Object(u.c)(f);return Object(h.jsxs)(O,{value:n,onChange:function(n,t){e(p(t))},"aria-label":"styled tabs example",children:[Object(h.jsx)(x,{value:"check",label:"\u041f\u0440\u043e\u0432\u0435\u0440\u0438\u0442\u044c"}),Object(h.jsx)(x,{value:"history",label:"\u0418\u0441\u0442\u043e\u0440\u0438\u044f"})]})}var k=t(13),v=t(177),y=t(164),C=t(178),w=t(32),S=t.n(w),T=t(48),z={categoriesList:[],selectedCategories:[],responseCategories:[],currentSubTasks:[],currentTask:[],error:null,selectedTaskId:null,isUploading:!1,isGettingTask:!0},L=Object(b.b)("check/getCategoriesThunk",function(){var e=Object(T.a)(S.a.mark((function e(n){var t;return S.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,fetch("/api/category_search?like="+n);case 2:return t=e.sent,e.next=5,t.json();case 5:return e.abrupt("return",e.sent);case 6:case"end":return e.stop()}}),e)})));return function(n){return e.apply(this,arguments)}}()),N=Object(b.b)("check/expressCheckThunk",function(){var e=Object(T.a)(S.a.mark((function e(n){var t;return S.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,fetch("/api/express",{method:"POST",headers:{"Content-Type":"application/json"},body:n});case 2:return t=e.sent,e.next=5,t.json();case 5:return e.abrupt("return",e.sent);case 6:case"end":return e.stop()}}),e)})));return function(n){return e.apply(this,arguments)}}()),W=Object(b.b)("check/sendFileThunk",function(){var e=Object(T.a)(S.a.mark((function e(n){var t,r;return S.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return t=n.body,n.fileName,e.next=3,fetch("/api/tasks",{method:"POST",body:t});case 3:return r=e.sent,e.next=6,r.json();case 6:return e.abrupt("return",e.sent);case 7:case"end":return e.stop()}}),e)})));return function(n){return e.apply(this,arguments)}}()),B=Object(b.b)("check/getLastTaskThunk",Object(T.a)(S.a.mark((function e(){var n;return S.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,fetch("/api/tasks/0");case 2:return n=e.sent,e.next=5,n.json();case 5:return e.abrupt("return",e.sent);case 6:case"end":return e.stop()}}),e)})))),J=Object(b.c)(Object(i.a)(Object(i.a)({name:"check",initialState:z},z),{},{reducers:{setSelectedCategories:function(e,n){e.selectedCategories.includes(JSON.stringify(n.payload))||e.selectedCategories.push(JSON.stringify(n.payload))},removeFromSelectedCategories:function(e,n){e.selectedCategories=e.selectedCategories.filter((function(e){return e!==n.payload}))},clearCategories:function(e){e.categoriesList=[]},setError:function(e,n){e.error=n.payload},clearAllCheckStates:function(e){e.categoriesList=[],e.selectedCategories=[],e.error=null},precheckCleaning:function(e){e.responseCategories=[],e.error=null}},extraReducers:function(e){e.addCase(L.fulfilled,(function(e,n){e.categoriesList=n.payload.categories})),e.addCase(N.fulfilled,(function(e,n){null===n.payload.isValid?e.error=null:e.error=!n.payload.isValid,e.responseCategories=n.payload.\u0441ategories,console.log(n.payload.\u0441ategories)})),e.addCase(B.fulfilled,(function(e,n){e.currentTask=n.payload.task,e.isGettingTask=!1})),e.addCase(B.pending,(function(e,n){e.isGettingTask=!0})),e.addCase(W.fulfilled,(function(e,n){console.log(n.payload.task),e.currentTask=n.payload.task,e.isUploading=!1})),e.addCase(W.pending,(function(e,n){e.isUploading=!0}))}})),M=J.actions,R=M.setSelectedCategories,U=M.removeFromSelectedCategories,V=M.clearCategories,E=M.clearAllCheckStates,I=M.precheckCleaning,P=function(e){return e.check.categoriesList},q=function(e){return e.check.selectedCategories},D=function(e){return e.check.error},F=function(e){return e.check.responseCategories},G=function(e){return e.check.currentSubTasks},A=function(e){return e.check.currentTask},$=function(e){return e.check.isUploading},_=function(e){return e.check.isGettingTask},H=J.reducer,K=t(166),Q=t(168),X=t(169);function Y(e){var n=e.task;return Object(h.jsx)(K.a,{sx:{minWidth:275,borderColor:"rgb(0,0,255,0.5)"},children:Object(h.jsxs)(Q.a,{children:[Object(h.jsx)(X.a,{sx:{fontSize:14},color:"text.secondary",gutterBottom:!0,children:"\u041f\u043e\u0441\u043b\u0435\u0434\u043d\u044f\u044f \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430"}),Object(h.jsxs)(X.a,{variant:"h5",component:"div",children:["\u041e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430 \u043e\u0442 ",n.time]}),Object(h.jsxs)(X.a,{variant:"h5",color:"rgb(0,0,255)",children:["\u0412 \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0435",Object(h.jsx)("br",{})]})]})})}var Z=t(170);function ee(e){var n=e.task;return Object(h.jsxs)(K.a,{sx:{minWidth:275,borderColor:"rgb(127,255,0,0.5)"},children:[Object(h.jsxs)(Q.a,{children:[Object(h.jsx)(X.a,{sx:{fontSize:14},color:"text.secondary",gutterBottom:!0,children:"\u041f\u043e\u0441\u043b\u0435\u0434\u043d\u044f\u044f \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430"}),Object(h.jsxs)(X.a,{variant:"h5",component:"div",children:["\u041e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430 \u043e\u0442 ",n.time]}),Object(h.jsxs)(X.a,{sx:{mb:1.5},color:"text.secondary",children:["\u0423\u0441\u043f\u0435\u0448\u043d\u043e: ",n.isValidCount," \u041e\u0448\u0438\u0431\u043a\u0430: ",n.inValidCount," \u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f \u043d\u0435 \u0443\u043a\u0430\u0437\u0430\u043d\u0430: ",n.notDetected]}),Object(h.jsxs)(X.a,{variant:"h5",color:"rgb(127,255,0)",children:["\u0417\u0430\u0432\u0435\u0440\u0448\u0435\u043d\u043e",Object(h.jsx)("br",{})]})]}),Object(h.jsx)(Z.a,{children:Object(h.jsx)(y.a,{size:"small",children:"\u041f\u043e\u0441\u043c\u043e\u0442\u0440\u0435\u0442\u044c \u0440\u0435\u0437\u0443\u043b\u044c\u0430\u0442"})})]})}t(172),t(176),t(175),t(171),t(173),t(174),t(167);function ne(){var e=Object(r.useState)(null),n=Object(k.a)(e,2),t=n[0],a=n[1],c=(Object(u.c)(G),Object(u.c)(A)),o=Object(u.c)($),i=Object(u.c)(_),s=Object(u.b)();return Object(r.useEffect)((function(){s(B())}),[]),Object(h.jsxs)("div",{style:re,children:[Object(h.jsx)("h1",{style:{marginLeft:"38%"},children:"\u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u0444\u0430\u0439\u043b\u0430"}),Object(h.jsx)("input",{type:"file",onChange:function(e){a(e.target.files[0])},id:"fileUpload",style:{display:"none"}}),Object(h.jsxs)(v.a,{style:{marginBottom:"1%"},children:[!o&&Object(h.jsx)(y.a,{variant:"contained",onClick:function(){document.querySelector("#fileUpload").click()},children:"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c"}),o&&Object(h.jsxs)("div",{children:[Object(h.jsx)(C.a,{})," \u0418\u0434\u0435\u0442 \u0437\u0430\u0433\u0440\u0443\u0437\u043a\u0430 \u0444\u0430\u0439\u043b\u0430"]}),!!t&&Object(h.jsx)(y.a,{onClick:function(){var e=new FormData;console.log(t),t&&(e.append("file",t),s(W({body:e,fileName:t.name})),a(null))},variant:"text",children:"\u041e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u044c"})]}),!!c&&!i&&"done"===c.status&&Object(h.jsx)(ee,{task:c}),!!c&&!i&&"run"===c.status&&Object(h.jsx)(Y,{task:c}),i&&Object(h.jsx)(C.a,{})]})}var te,re={border:"solid rgb(0,0,0,0.1)",padding:"1%",paddingBottom:"1%",margin:"1%"},ae=t(160),ce=t(85),oe=t(23),ie=t(83),se=t.n(ie),le=t(82),de=t.n(le),ue=["label","onDelete","el"],be=Object(s.a)("div")((function(e){var n=e.theme;return"\n  color: ".concat("dark"===n.palette.mode?"rgba(255,255,255,0.65)":"rgba(0,0,0,.85)",";\n  font-size: 14px;\n")})),je=(Object(s.a)("label")(te||(te=Object(oe.a)(["\n  padding: 0 0 4px;\n  line-height: 1.5;\n  display: block;\n"]))),Object(s.a)("div")((function(e){var n=e.theme;return"\n  width: 300px;\n  border: 1px solid ".concat("dark"===n.palette.mode?"#434343":"#d9d9d9",";\n  background-color: ").concat("dark"===n.palette.mode?"#141414":"#fff",";\n  border-radius: 4px;\n  padding: 1px;\n  display: flex;\n  flex-wrap: wrap;\n\n  &:hover {\n    border-color: ").concat("dark"===n.palette.mode?"#177ddc":"#40a9ff",";\n  }\n\n  &.focused {\n    border-color: ").concat("dark"===n.palette.mode?"#177ddc":"#40a9ff",";\n    box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);\n  }\n\n  & input {\n    background-color: ").concat("dark"===n.palette.mode?"#141414":"#fff",";\n    color: ").concat("dark"===n.palette.mode?"rgba(255,255,255,0.65)":"rgba(0,0,0,.85)",";\n    height:37px ;\n    box-sizing: border-box;\n    padding: 4px 6px;\n    width: 0;\n    min-width: 30px;\n    flex-grow: 1;\n    border: 0;\n    margin: 0;\n    outline: 0;\n  }\n")})));var pe=Object(s.a)((function(e){var n=e.label,t=(e.onDelete,e.el),r=Object(ce.a)(e,ue),a=Object(u.b)();return Object(h.jsxs)("div",Object(i.a)(Object(i.a)({},r),{},{children:[Object(h.jsx)("span",{children:n}),Object(h.jsx)(de.a,{onClick:function(){a(U(t))}})]}))}))((function(e){var n=e.theme;return"\n  display: flex;\n  align-items: center;\n  height: 24px;\n  margin: 2px;\n  line-height: 22px;\n  background-color: ".concat("dark"===n.palette.mode?"rgba(255,255,255,0.08)":"#fafafa",";\n  border: 1px solid ").concat("dark"===n.palette.mode?"#303030":"#e8e8e8",";\n  border-radius: 2px;\n  box-sizing: content-box;\n  padding: 0 4px 0 10px;\n  outline: 0;\n  overflow: hidden;\n\n  &:focus {\n    border-color: ").concat("dark"===n.palette.mode?"#177ddc":"#40a9ff",";\n    background-color: ").concat("dark"===n.palette.mode?"#003b57":"#e6f7ff",";\n  }\n\n  & span {\n    overflow: hidden;\n    white-space: nowrap;\n    text-overflow: ellipsis;\n  }\n\n  & svg {\n    font-size: 12px;\n    cursor: pointer;\n    padding: 4px;\n  }\n")})),fe=Object(s.a)("ul")((function(e){var n=e.theme;return"\n  width: 300px;\n  margin: 2px 0 0;\n  padding: 0;\n  position: absolute;\n  list-style: none;\n  background-color: ".concat("dark"===n.palette.mode?"#141414":"#fff",";\n  overflow: auto;\n  max-height: 250px;\n  border-radius: 4px;\n  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);\n  z-index: 1;\n\n  & li {\n    padding: 5px 12px;\n    display: flex;\n\n    & span {\n      flex-grow: 1;\n    }\n\n    & svg {\n      color: transparent;\n    }\n  }\n\n  & li[aria-selected='true'] {\n    background-color: ").concat("dark"===n.palette.mode?"#2b2b2b":"#fafafa",";\n    font-weight: 600;\n\n    & svg {\n      color: #1890ff;\n    }\n  }\n\n  & li[data-focus='true'] {\n    background-color: ").concat("dark"===n.palette.mode?"#003b57":"#e6f7ff",";\n    cursor: pointer;\n\n    & svg {\n      color: currentColor;\n    }\n  }\n")}));function ge(){var e=Object(u.c)(P),n=Object(u.c)(q),t=Object(u.b)();return Object(h.jsxs)(be,{children:[Object(h.jsx)("div",{children:Object(h.jsxs)(je,{children:[n.map((function(e,n){return Object(h.jsx)(pe,{label:JSON.parse(e).name,el:e})})),Object(h.jsx)("input",{id:"categoryInput",spellcheck:"false",placeholder:"\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f",onChange:function(e){e.target.value.length?t(L(e.target.value)):t(V())}})]})}),e.length>0?Object(h.jsx)(fe,{children:e.map((function(e,n){return Object(h.jsxs)("li",{onClick:function(n){t(V()),document.querySelector("#categoryInput").value="",t(R(e))},children:[Object(h.jsx)("span",{children:e.name}),Object(h.jsx)(se.a,{fontSize:"small"})]})}))}):null]})}function he(){var e=Object(r.useState)("solid rgb(0,0,0,0.1)"),n=Object(k.a)(e,2),t=n[0],a=n[1],c=Object(u.c)(D),o=Object(u.c)(q),s=Object(u.c)(F),l=Object(u.b)();return Object(r.useEffect)((function(){a(null===c?"solid rgb(0,0,0,0.1)":c?"solid rgb(255,0,0,0.7)":"solid rgb(127,255,0,0.5)")}),[c]),Object(h.jsxs)("div",{style:Object(i.a)(Object(i.a)({},xe),{},{border:t}),children:[Object(h.jsx)("h1",{style:{marginLeft:"38%"},children:"\u0411\u044b\u0441\u0442\u0440\u0430\u044f \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0430"}),Object(h.jsxs)(v.a,{component:"form",sx:{"& > :not(style)":{m:2,display:"inline-block"}},noValidate:!0,autoComplete:"off",children:[Object(h.jsx)(ae.a,{style:{width:"45%",marginRight:"1%"},fullWidth:!0,id:"productName",label:"\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430",variant:"outlined",size:"small"}),Object(h.jsx)(ge,{}),Object(h.jsx)(y.a,{onClick:function(){var e=document.querySelector("#productName").value,n=o.map((function(e){return JSON.parse(e).code})),t=JSON.stringify({name:e,codes:n});l(I()),l(N(t))},variant:"contained",color:"success",children:"\u041f\u0440\u043e\u0432\u0435\u0440\u0438\u0442\u044c"}),Object(h.jsx)(y.a,{variant:"outlined",color:"error",onClick:function(){document.querySelector("#productName").value="",l(E())},children:"\u041e\u0447\u0438\u0441\u0442\u0438\u0442\u044c"})]}),!0===c&&Object(h.jsx)("p",{style:{marginLeft:"45%",color:"red"},children:"\u041e\u0448\u0438\u0431\u043a\u0430"}),!0===c&&s&&Object(h.jsxs)("p",{style:{marginLeft:"1%"},children:["\u041f\u0440\u0435\u0434\u043f\u043e\u043b\u0430\u0433\u0430\u0435\u043c\u044b\u0435 \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438: ",s.map((function(e){return e.name+"; "}))]}),!1===c&&Object(h.jsx)("p",{style:{marginLeft:"40%",color:"green"},children:"\u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u0443\u0441\u043f\u0435\u0448\u043d\u043e \u043f\u0440\u043e\u0439\u0434\u0435\u043d\u0430"})]})}var xe={padding:"1%",paddingBottom:"1%",margin:"1%"};function Oe(){return Object(h.jsxs)("div",{children:[Object(h.jsx)(he,{}),Object(h.jsx)("br",{}),Object(h.jsx)("br",{}),Object(h.jsx)(ne,{})]})}var me=function(){var e=Object(u.c)(f);return Object(r.useEffect)((function(){console.log(e)}),[e]),Object(h.jsxs)("div",{children:[Object(h.jsx)(m,{}),"check"===e&&Object(h.jsx)(Oe,{})]})},ke=Object(b.a)({reducer:{navigation:g,check:H}});Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));o.a.render(Object(h.jsx)(a.a.StrictMode,{children:Object(h.jsx)(u.a,{store:ke,children:Object(h.jsx)(me,{})})}),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then((function(e){e.unregister()}))}},[[112,1,2]]]);
//# sourceMappingURL=main.67ad184b.chunk.js.map