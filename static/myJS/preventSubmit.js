// const collectBtn = document.getElementById('editable-sample_new');
// const submitBtn = document.querySelector('button[type="submit"]');
//
// let isInfoCollected = false;
//
// collectBtn.addEventListener('click', () => {
//   isInfoCollected = true;
// });
//
// submitBtn.addEventListener('click', (event) => {
//   if (!isInfoCollected) {
//     event.preventDefault(); // 阻止表单提交
//     submitBtn.disabled = true; // 禁用提交按钮
//     alert('请先采集信息'); // 显示提示信息
//   }
// });
// 获取收集人脸信息按钮和提交按钮
// const collectBtn = document.getElementById("collect_photos");
// const submitBtn = document.querySelector("button[id='submitBtn']");
//
// // 初始化提交按钮为不可用
// submitBtn.disabled = true;
//
// // 点击收集人脸信息按钮时，提交按钮可用
// collectBtn.addEventListener("click", function() {
//     submitBtn.disabled = false;
// });
var submitBtn = document.querySelector("button[type='submit']");
var collectBtn = document.querySelector("#collect_photos");
submitBtn.disabled = true;

function checkFaceInfo() {
  submitBtn.disabled = localStorage.getItem("hasCollectedFace") !== "true";
}

checkFaceInfo();
collectBtn.addEventListener("click", function() {
  localStorage.setItem("hasCollectedFace", "true");
  checkFaceInfo();
});
