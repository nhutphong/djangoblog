// suppose the `id` attribute of element is `message_container`.
var message_ele = document.getElementById("msg");

setTimeout(function(){ 
   message_ele.style.display = "none"; 
}, 3000);
// Timeout is 3 sec, you can change it