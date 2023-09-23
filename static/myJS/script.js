function show(){
    //显示div
     document.getElementById("form").style.display="block";
    //隐藏
    //document.getElementByID("form").style.display="none";

    var obj={
      name:'张三',
      is_holder:1,
      phone_num:17596239368
      }

     document.getElementById("name").value = obj.name
     document.getElementById("is_holder").value = obj.is_holder
     document.getElementById("phone_num").value = obj.phone_num

     }

function switchDarkMode() {
   var element = document.body;
   element.classList.toggle("dark_mode");
}
function showPopup(id) {
        var popup = document.getElementById("popup_" + id);
        popup.style.display = "block";
}

function hidePopup(id) {
    var popup = document.getElementById("popup_" + id);
    popup.style.display = "none";
}

function saveInfo() {
    // Do something with the entered info here
    hidePopup();
}


function exportToExcel(){
    alert('已经导出到桌面')
}

function printPage() {
  window.print();
}

