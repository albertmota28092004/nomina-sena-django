(function () {
  "use strict";

  // ======= Sticky
  window.onscroll = function () {
    const ud_header = document.querySelector(".ud-header");
    const sticky = ud_header.offsetTop;
    const logo = document.querySelector(".header-logo");

    // Verifica si está en modo oscuro
    const isDarkMode = document.documentElement.classList.contains("dark");

    if (window.pageYOffset > sticky) {
      ud_header.classList.add("sticky");
    } else {
      ud_header.classList.remove("sticky");
    }

    // Aplicar clase para modo claro u oscuro en la navbar sticky
    if (ud_header.classList.contains("sticky")) {
      if (isDarkMode) {
        ud_header.classList.add("dark-mode");
        ud_header.classList.remove("light-mode");
      } else {
        ud_header.classList.add("light-mode");
        ud_header.classList.remove("dark-mode");
      }
    } else {
      // Remover clases si no está sticky
      ud_header.classList.remove("dark-mode", "light-mode");
    }

    // Mostrar u ocultar el botón de "back-to-top"
    const backToTop = document.querySelector(".back-to-top");
    if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
      backToTop.style.display = "flex";
    } else {
      backToTop.style.display = "none";
    }
  };

  // Para asegurarte de que el logo cambia correctamente al cargar la página
  document.addEventListener("DOMContentLoaded", function () {
    const ud_header = document.querySelector(".ud-header");
    const logo = document.querySelector(".header-logo");
    const isDarkMode = document.documentElement.classList.contains("dark");

    // Aplicar clase para modo claro u oscuro en la navbar
    if (isDarkMode) {
      ud_header.classList.add("dark-mode");
    } else {
      ud_header.classList.remove("dark-mode");
    }
  });

  // ===== responsive navbar
  let navbarToggler = document.querySelector("#navbarToggler");
  const navbarCollapse = document.querySelector("#navbarCollapse");

  navbarToggler.addEventListener("click", () => {
    navbarToggler.classList.toggle("navbarTogglerActive");
    navbarCollapse.classList.toggle("hidden");

    // Comprobar condiciones de modo oscuro y tamaño de pantalla
    const isDarkMode = document.documentElement.classList.contains("dark");
    const isSmallScreen = window.innerWidth <= 540;

    if (isDarkMode && isSmallScreen) {
      navbarCollapse.classList.add("dark-navbar-collapse");

    } else {
      navbarCollapse.classList.remove("dark-navbar-collapse");
    }
  });

  //===== close navbar-collapse when a link clicked
  document
    .querySelectorAll("#navbarCollapse ul li:not(.submenu-item) a")
    .forEach((e) =>
      e.addEventListener("click", () => {
        navbarToggler.classList.remove("navbarTogglerActive");
        navbarCollapse.classList.add("hidden");
      })
    );

  // ===== Sub-menu
  const submenuItems = document.querySelectorAll(".submenu-item");
  submenuItems.forEach((el) => {
    el.querySelector("a").addEventListener("click", () => {
      el.querySelector(".submenu").classList.toggle("hidden");
    });
  });

  // ===== Faq accordion
  const faqs = document.querySelectorAll(".single-faq");
  faqs.forEach((el) => {
    el.querySelector(".faq-btn").addEventListener("click", () => {
      el.querySelector(".icon").classList.toggle("rotate-180");
      el.querySelector(".faq-content").classList.toggle("hidden");
    });
  });

  // ===== wow js
  new WOW().init();

  // ====== scroll top js
  function scrollTo(element, to = 0, duration = 500) {
    const start = element.scrollTop;
    const change = to - start;
    const increment = 20;
    let currentTime = 0;

    const animateScroll = () => {
      currentTime += increment;

      const val = Math.easeInOutQuad(currentTime, start, change, duration);

      element.scrollTop = val;

      if (currentTime < duration) {
        setTimeout(animateScroll, increment);
      }
    };

    animateScroll();
  }

  Math.easeInOutQuad = function (t, b, c, d) {
    t /= d / 2;
    if (t < 1) return (c / 2) * t * t + b;
    t--;
    return (-c / 2) * (t * (t - 2) - 1) + b;
  };

  document.querySelector(".back-to-top").onclick = () => {
    scrollTo(document.documentElement);
  };

  /* ========  themeSwitcher start ========= */

  // themeSwitcher
  const themeSwitcher = document.getElementById('themeSwitcher');

  // Theme Vars
  const userTheme = localStorage.getItem('theme');
  const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches;

  // Initial Theme Check
  const themeCheck = () => {
    if (userTheme === 'dark' || (!userTheme && systemTheme)) {
      document.documentElement.classList.add('dark');
      return;
    }
  };

  // Manual Theme Switch
  const themeSwitch = () => {
    if (document.documentElement.classList.contains('dark')) {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
      return;
    }

    document.documentElement.classList.add('dark');
    localStorage.setItem('theme', 'dark');
  };

  // call theme switch on clicking buttons
  themeSwitcher.addEventListener('click', () => {
    themeSwitch();

    // Comprobar condiciones de modo oscuro y tamaño de pantalla
    const isDarkMode = document.documentElement.classList.contains("dark");
    const isSmallScreen = window.innerWidth <= 540;

    if (isDarkMode && isSmallScreen) {
      navbarCollapse.classList.add("dark-navbar-collapse");
    } else {
      navbarCollapse.classList.remove("dark-navbar-collapse");
    }
  });

  // invoke theme check on initial load
  themeCheck();
  /* ========  themeSwitcher End ========= */
})();

const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))