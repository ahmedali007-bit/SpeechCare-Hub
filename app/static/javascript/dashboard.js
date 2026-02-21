$.sidebarMenu = function (menu) {
  var animationSpeed = 300;

  $(menu).on("click", "li a", function (e) {
    var $this = $(this);
    var checkElement = $this.next();

    if (checkElement.is(".treeview-menu") && checkElement.is(":visible")) {
      checkElement.slideUp(animationSpeed, function () {
        checkElement.removeClass("menu-open");
      });
      checkElement.parent("li").removeClass("active");
    }

    //If the menu is not visible
    else if (
      checkElement.is(".treeview-menu") &&
      !checkElement.is(":visible")
    ) {
      //Get the parent menu
      var parent = $this.parents("ul").first();
      //Close all open menus within the parent
      var ul = parent.find("ul:visible").slideUp(animationSpeed);
      //Remove the menu-open class from the parent
      ul.removeClass("menu-open");
      //Get the parent li
      var parent_li = $this.parent("li");

      //Open the target menu and add the menu-open class
      checkElement.slideDown(animationSpeed, function () {
        //Add the class active to the parent li
        checkElement.addClass("menu-open");
        parent.find("li.active").removeClass("active");
        parent_li.addClass("active");
      });
    }
    //if this isn't a link, prevent the page from being redirected
    if (checkElement.is(".treeview-menu")) {
      e.preventDefault();
    }
  });
};
$.sidebarMenu($(".sidebar-menu"));

// Custom Sidebar JS
jQuery(function ($) {
  //toggle sidebar
  $(".toggle-sidebar").on("click", function () {
    $(".page-wrapper").toggleClass("toggled");
  });

  // Pin sidebar on click
  $(".pin-sidebar").on("click", function () {
    if ($(".page-wrapper").hasClass("pinned")) {
      // unpin sidebar when hovered
      $(".page-wrapper").removeClass("pinned");
      $("#sidebar").unbind("hover");
    } else {
      $(".page-wrapper").addClass("pinned");
      $("#sidebar").hover(
        function () {
          console.log("mouseenter");
          $(".page-wrapper").addClass("sidebar-hovered");
        },
        function () {
          console.log("mouseout");
          $(".page-wrapper").removeClass("sidebar-hovered");
        }
      );
    }
  });

  // Pinned sidebar
  $(function () {
    $(".page-wrapper").hasClass("pinned");
    $("#sidebar").hover(
      function () {
        console.log("mouseenter");
        $(".page-wrapper").addClass("sidebar-hovered");
      },
      function () {
        console.log("mouseout");
        $(".page-wrapper").removeClass("sidebar-hovered");
      }
    );
  });

  // Toggle sidebar overlay
  $("#overlay").on("click", function () {
    $(".page-wrapper").toggleClass("toggled");
  });

  // Added by Srinu
  $(function () {
    // When the window is resized,
    $(window).resize(function () {
      // When the width and height meet your specific requirements or lower
      if ($(window).width() <= 768) {
        $(".page-wrapper").removeClass("pinned");
      }
    });
    // When the window is resized,
    $(window).resize(function () {
      // When the width and height meet your specific requirements or lower
      if ($(window).width() >= 768) {
        $(".page-wrapper").removeClass("toggled");
      }
    });
  });
});

// Loading
$(function () {
  $("#loading-wrapper").fadeOut(2000);
});

$(function () {
  $(".day-sorting .btn").on("click", function () {
    $(".day-sorting .btn").removeClass("btn-primary");
    $(this).addClass("btn-primary");
  });
});


/***********
***********
***********
  Bootstrap JS 
***********
***********
***********/

// // Tooltip
// var tooltipTriggerList = [].slice.call(
//   document.querySelectorAll('[data-bs-toggle="tooltip"]')
// );
// var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
//   return new bootstrap.Tooltip(tooltipTriggerEl);
// });

// Popover
var popoverTriggerList = [].slice.call(
  document.querySelectorAll('[data-bs-toggle="popover"]')
);
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl);
});

  // Doughnut Chart for Therapy Progress
  $(document).ready(function () {
    const therapyProgressData = {
      labels: ['Completed', 'Remaining'],
      datasets: [{
        label: 'Therapy Progress',
        data: [75, 25], // Replace 75 with dynamic progress percentage
        backgroundColor: [
          'rgba(23, 143, 119, 0.5)', // Completed - Green
          'rgba(255, 90, 57,0.5)'  // Remaining - Red
        ],
        borderColor: [
          'rgba(23, 143, 119, 0.5)',
          'rgba(255, 90, 57,0.5)'
        ],
        borderWidth: 1
      }]
    };

    const therapyProgressOptions = {
      responsive: true,
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            font: {
              size: 10
            }
          }
        }
      }
    };

    const therapyProgressCtx = $('#therapyProgressChart')[0].getContext('2d');
    new Chart(therapyProgressCtx, {
      type: 'doughnut',
      data: therapyProgressData,
      options: therapyProgressOptions
    });

    // Calendar Generation
    const sessions = [
      { date: '2025-01-25', label: 'Christmas Therapy' },
      { date: '2025-01-08', label: 'Final Assessment' }
    ];

    function generateCalendar(year, month) {
      const $calendar = $('.calendar');
      const date = new Date(year, month, 1);
      const today = new Date();
      const daysInMonth = new Date(year, month + 1, 0).getDate();
      const firstDay = date.getDay();

      // Clear existing calendar days
      $calendar.find('.day:not(.day-header)').remove();

      // Add empty days for the start of the month
      for (let i = 0; i < firstDay; i++) {
        $calendar.append('<div class="day"></div>');
      }

      // Add days of the month
      for (let i = 1; i <= daysInMonth; i++) {
        const dayString = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
        const session = sessions.find(s => s.date === dayString);
        const $dayDiv = $(`<div class="day ${session ? 'session-day' : ''}">${i}</div>`);

        if (session) {
          $dayDiv.attr('title', session.label); // Tooltip for session details
        }

        if (today.getFullYear() === year && today.getMonth() === month && today.getDate() === i) {
          $dayDiv.css('border', '2px solid rgba(23, 143, 119, 0.9)');
        }

        $calendar.append($dayDiv);
      }
    }

    // Generate the current month's calendar
    const today = new Date();
    generateCalendar(today.getFullYear(), today.getMonth());

    // Weekly Progress Chart
    const weeklyProgressData = {
      labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], // Days of the week
      datasets: [{
        label: 'Tasks Completed',
        data: [3, 5, 2, 4, 6, 7, 5], // Sample data points
        backgroundColor: [
          'rgba(75, 192, 192, 0.6)', // Colors for bars
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(153, 102, 255, 0.6)',
          'rgba(255, 99, 132, 0.6)',
          'rgba(255, 159, 64, 0.6)',
          'rgba(201, 203, 207, 0.6)',
        ],
        borderColor: [
          'rgba(75, 192, 192, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(153, 102, 255, 1)',
          'rgba(255, 99, 132, 1)',
          'rgba(255, 159, 64, 1)',
          'rgba(201, 203, 207, 1)',
        ],
        borderWidth: 1, // Bar border width
      }]
    };

    const weeklyProgressOptions = {
      responsive: true,
      plugins: {
        legend: {
          display: true,
          position: 'top',
        },
        title: {
          display: true,
          text: 'Weekly Therapy Task Completion',
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            stepSize: 1, // Increment for Y-axis
          },
        },
      },
    };

    const weeklyProgressCtx = $('#weeklyProgressChart')[0].getContext('2d');
    new Chart(weeklyProgressCtx, {
      type: 'bar',
      data: weeklyProgressData,
      options: weeklyProgressOptions
    });
  });

  $(document).ready(function () {
    $('.sidebar-link').on('click', function () {
      // Remove 'active' and 'current-page' classes from all <li> elements
      $('.sidebar-menu li').removeClass('active current-page');
      // Add 'active' and 'current-page' classes to the clicked link's parent <li>
      $(this).parent().addClass('active current-page');
    });
  });

  
  
  
  