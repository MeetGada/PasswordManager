
// For hiding the navigation-bar

 var close_menu = document.querySelector(".menu-bar-close").addEventListener("click",() => {nav_collapse(),badge_return_pos()});

 function nav_collapse(){
   document.querySelector(".nav-bar").classList.add("nav-collapse");
 }

 function badge_return_pos() {
     document.querySelector(".badge").classList.remove("badge-move");
 }

// For opening navigation-bar

var open_menu = document.querySelector(".menu-bar-open").addEventListener("click",() => {open_nav_bar(); move_badge();});

function open_nav_bar() {
   document.querySelector(".nav-bar").classList.remove("nav-collapse")
}

function move_badge() {
    document.querySelector(".badge").classList.add("badge-move")
}

// For generating password


  function pass_generator(){  

  var  password_length = document.querySelector("#pass-length").value;
  
  var generated_pass = "";
  
  var characters = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ$#&" 
  
  charactersLength = characters.length; 
  
  for (var i=0; i < password_length; i++) {
  
    generated_pass += characters.charAt(Math.floor(Math.random() * charactersLength) +1);
  
  }
  document.querySelector("#pass").value = generated_pass;
  }



document.querySelector(".generate-btn").addEventListener("click",pass_generator);

// For copying the generated passwor


function copy_data(pass) {
  var range = document.createRange();
  range.selectNode(pass); 
  window.getSelection().removeAllRanges(); //removes previous selection text
  window.getSelection().addRange(range);  //and add the current range (selection)
  document.execCommand("copy");           // copy selected text in pass node
  window.getSelection().removeAllRanges();// then remove the selection
  alert("Password Copied!!!");
}

