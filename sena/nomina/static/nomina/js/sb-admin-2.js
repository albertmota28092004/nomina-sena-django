$(document).ready(function() {
  "use strict";

  // Toggle the side navigation
  $(document).on('click', '#sidebarToggle', function(e) {
    e.preventDefault();
    $("body").toggleClass("sidebar-toggled");
    $(".sidebar").toggleClass("toggled");
    if ($(".sidebar").hasClass("toggled")) {
      $('.sidebar .collapse').collapse('hide');
    };
  });

  // Close any open menu accordions when window is resized below 768px
  $(window).resize(function() {
    if ($(window).width() < 768) {
      $('.sidebar .collapse').collapse('hide');
    };

    // Toggle the side navigation when window is resized below 480px
    if ($(window).width() < 480 && !$(".sidebar").hasClass("toggled")) {
      $("body").addClass("sidebar-toggled");
      $(".sidebar").addClass("toggled");
      $('.sidebar .collapse').collapse('hide');
    };
  });

  // Prevent the content wrapper from scrolling when the fixed side navigation hovered over
  $('body.fixed-nav .sidebar').on('mousewheel DOMMouseScroll wheel', function(e) {
    if ($(window).width() > 768) {
      var e0 = e.originalEvent,
        delta = e0.wheelDelta || -e0.detail;
      this.scrollTop += (delta < 0 ? 1 : -1) * 30;
      e.preventDefault();
    }
  });

  // Scroll to top button appear
  $(document).on('scroll', function() {
    var scrollDistance = $(this).scrollTop();
    if (scrollDistance > 100) {
      $('.scroll-to-top').fadeIn();
    } else {
      $('.scroll-to-top').fadeOut();
    }
  });

  // Smooth scrolling using jQuery easing
  $(document).on('click', 'a.scroll-to-top', function(e) {
    var $anchor = $(this);
    $('html, body').stop().animate({
      scrollTop: ($($anchor.attr('href')).offset().top)
    }, 1000, 'easeInOutExpo');
    e.preventDefault();
  });
});




document.addEventListener("DOMContentLoaded", function() {
   // Obtener el identificador único de la página actual
   var currentPageId = document.body.id;

   // Obtener todos los elementos li de la barra lateral
   var sidebarItems = document.querySelectorAll("#accordionSidebar li.nav-item");

   // Iterar sobre los elementos li y agregar la clase 'active' al elemento correspondiente
   sidebarItems.forEach(function(item) {
       var link = item.querySelector("a.nav-link");
       var href = link.getAttribute("href");

       // Comparar el href del enlace con el identificador único de la página actual
       if (href === currentPageId || (currentPageId.startsWith(href) && href !== "#")) {
           item.classList.add("active");
           // Expandir el menú si es un elemento de menú desplegable
           if (item.classList.contains("collapse")) {
               item.querySelector(".collapse").classList.add("show");
           }
       }
   });
});

document.querySelectorAll('.custom-tooltip').forEach(item => {
  item.addEventListener('focus', function() {
      this.classList.add('active');
  });
  item.addEventListener('blur', function() {
      this.classList.remove('active');
  });
});
