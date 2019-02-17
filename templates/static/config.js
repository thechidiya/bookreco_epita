document.addEventListener("DOMContentLoaded", function(){
    document.getElementById("btRegister").addEventListener("click", function(e){
  		e.preventDefault();
	});
  document.getElementById("btnClear").addEventListener("click", function(e){
      e.preventDefault();
      var inputs = document.getElementsByClassName('check');
      for(var i=0;i<inputs.length;i++){
        inputs[i].checked = false;
      }
  });
  document.getElementById("btnMark").addEventListener("click", function(e){
      e.preventDefault();
      var inputs = document.getElementsByClassName('check');
      for(var i=0;i<inputs.length;i++){
        inputs[i].checked = true;
      }
  });
  document.getElementById("btnDelete").addEventListener("click", function(e){
      e.preventDefault();
      var node = document.getElementById("myList");
      while (node.firstChild) {
        node.removeChild(node.firstChild);
      }
  });
});