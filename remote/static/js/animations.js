function reveal() {
    var reveals = document.querySelectorAll(".animbaseoff");
  
    for (var i = 0; i < reveals.length; i++) {
      var windowHeight = window.innerHeight;
      var elementTop = reveals[i].getBoundingClientRect().top;
      var elementVisible = 0;
  
      if (elementTop < windowHeight - elementVisible) {
        
        
        reveals[i].classList.remove("animbaseoff");
        reveals[i].classList.add("animbase");
      }
      /*
      Not needed
      else {
        reveals[i].classList.remove("active");
      }
      */
  
    }
  }
  
  window.addEventListener("scroll", reveal);