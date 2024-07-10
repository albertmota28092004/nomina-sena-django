const pageLink = document.querySelectorAll(".ud-menu-scroll");

pageLink.forEach((elem) => {
  elem.addEventListener("click", (e) => {
    e.preventDefault();
    document.querySelector(elem.getAttribute("href")).scrollIntoView({
      behavior: "smooth",
      offsetTop: 1 - 60,
    });
  });
});

// section menu active
function onScroll(event) {
  const sections = document.querySelectorAll(".ud-menu-scroll");
  const scrollPos =
    window.pageYOffset ||
    document.documentElement.scrollTop ||
    document.body.scrollTop;

  for (let i = 0; i < sections.length; i++) {
    const currLink = sections[i];
    const val = currLink.getAttribute("href");
    const refElement = document.querySelector(val);
    const scrollTopMinus = scrollPos + 73;
    if (
      refElement.offsetTop <= scrollTopMinus &&
      refElement.offsetTop + refElement.offsetHeight > scrollTopMinus
    ) {
      document
        .querySelector(".ud-menu-scroll")
        .classList.remove("active");
      currLink.classList.add("active");
    } else {
      currLink.classList.remove("active");
    }
  }
}

window.document.addEventListener("scroll", onScroll);

// Testimonial
const testimonialSwiper = new Swiper(".testimonial-carousel", {
  slidesPerView: 1,
  spaceBetween: 30,

  // Navigation arrows
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },

  breakpoints: {
    640: {
      slidesPerView: 2,
      spaceBetween: 30,
    },
    1024: {
      slidesPerView: 3,
      spaceBetween: 30,
    },
    1280: {
      slidesPerView: 3,
      spaceBetween: 30,
    },
  },
});

// ------------------------------- 


document.addEventListener("DOMContentLoaded", function () {
  const pestanas = document.querySelectorAll(".nav-item");
  const secciones = document.querySelectorAll("section");
  const navbarCollapse = document.querySelector("#navbarCollapse");

  function actualizarBarra() {
    // Check if the navbar is collapsed
    if (window.innerWidth <= 540 || !navbarCollapse.classList.contains("hidden")) {
      // Remove existing bar if it exists
      document.querySelectorAll('.barra-verde').forEach(barra => barra.remove());
      return; // Exit the function early
    }

    let seccionActual = null;

    secciones.forEach(seccion => {
      const rect = seccion.getBoundingClientRect();
      if (rect.top >= 0 && rect.top < window.innerHeight / 2) {
        seccionActual = seccion;
      }
    });

    if (seccionActual) {
      const idSeccionActual = seccionActual.getAttribute('id');
      const navItemActual = document.querySelector(`.nav-item a[href="#${idSeccionActual}"]`).parentElement;

      // Remove active class from all nav items
      pestanas.forEach(p => p.classList.remove('active'));

      // Add active class to the current nav item
      navItemActual.classList.add('active');

      // Remove existing bar
      document.querySelectorAll('.barra-verde').forEach(barra => barra.remove());

      // Create and add the bar to the active nav item
      const barra = document.createElement('div');
      barra.classList.add('barra-verde');
      navItemActual.appendChild(barra);

      // Adjust the width of the bar to match the text width
      const link = navItemActual.querySelector('a');
      barra.style.width = `${link.offsetWidth}px`;

      // Set the color based on the mode
      const isDarkMode = document.documentElement.classList.contains('dark');
      if (isDarkMode) {
        barra.style.backgroundColor = '#85EA00'; // Green for dark mode
      } else {
        barra.style.backgroundColor = '#102530'; // #102530 for normal mode
      }
    }
  }

  pestanas.forEach(pestana => {
    const link = pestana.querySelector('a');
    link.addEventListener('click', function () {
      // Remove active class from all nav items
      pestanas.forEach(p => p.classList.remove('active'));

      // Add active class to the clicked nav item
      pestana.classList.add('active');

      // Remove existing bar
      document.querySelectorAll('.barra-verde').forEach(barra => barra.remove());

      // Create and add the bar to the active nav item
      const barra = document.createElement('div');
      barra.classList.add('barra-verde');
      pestana.appendChild(barra);

      // Adjust the width of the bar to match the text width
      barra.style.width = `${link.offsetWidth}px`;

      // Set the color based on the mode
      const isDarkMode = document.documentElement.classList.contains('dark');
      if (isDarkMode) {
        barra.style.backgroundColor = '#3758F9'; // Green for dark mode
      } else {
        barra.style.backgroundColor = '#102530'; // #102530 for normal mode
      }
    });
  });

  // Initial setup to add the bar to the active nav item
  const activePestana = document.querySelector('.nav-item.active');
  if (activePestana) {
    const barra = document.createElement('div');
    barra.classList.add('barra-verde');
    activePestana.appendChild(barra);

    // Adjust the width of the bar to match the text width
    const link = activePestana.querySelector('a');
    barra.style.width = `${link.offsetWidth}px`;

    // Set the color based on the mode
    const isDarkMode = document.documentElement.classList.contains('dark');
    if (isDarkMode) {
      barra.style.backgroundColor = '#3758F9'; // Green for dark mode
    } else {
      barra.style.backgroundColor = '#102530'; // #102530 for normal mode
    }
  }

  // Add scroll event listener to update the bar on scroll
  window.addEventListener('scroll', actualizarBarra);

  // Add resize event listener to update the bar visibility on resize
  window.addEventListener('resize', actualizarBarra);

  // Initial call to update the bar based on current scroll position
  actualizarBarra();
});




