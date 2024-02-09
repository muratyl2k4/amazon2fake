// navbar menu bars
let menu = document.querySelector("#menu-bars");
let nav = document.querySelector(".navbar");

menu.onclick = () => { 
    menu.classList.toggle("fa-times");
    nav.classList.toggle("active");
}

// navbar dark mode 


function setDarkMode(){ 
    /*
    document.documentElement.style.setProperty('--white', 'black');
    document.documentElement.style.setProperty('--bsr-primary', 'orange');
    document.documentElement.style.setProperty('--black', 'white');
    document.documentElement.style.setProperty('--bsr-a', 'white');

    */
}

const onScroll = () => {

    const scroll = document.documentElement.scrollTop

    if (scroll > 40) {
    header.classList.add('shrink')
    } else {
    header.classList.remove('shrink')
    }
}
window.addEventListener('scroll', onScroll)
  
    