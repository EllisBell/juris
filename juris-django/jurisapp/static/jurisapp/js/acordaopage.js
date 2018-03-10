$(document).ready(function() {

    /****************** acordao page **********************/

   function fixSidebarWhenScrollingOnWideScreen() {
   	var sidebar = $('#ac-sidebar');
   	if($(window).width() >= 900) {		
		var topOfSidebar = sidebar.offset().top - parseFloat(sidebar.css('margin-top'));

		$(window).scroll(function (event) {
	      var y = $(this).scrollTop();
          var scrollBelowTopOfSidebar = (y >= topOfSidebar);
          if (scrollBelowTopOfSidebar) {
	        sidebar.css("position", "fixed");
	        sidebar.css("top",  0);
	      } else {
	        sidebar.css("position", "static");
	      }
		});			
	}
	else {
		sidebar.css("position", "static");
		$(window).off('scroll');
	}
   }

   fixSidebarWhenScrollingOnWideScreen();

   $(window).resize(function() {
   	fixSidebarWhenScrollingOnWideScreen();
   });

});