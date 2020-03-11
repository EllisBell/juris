$(document).ready(function() {

    /****************** acordao page **********************/

   function fixSidebarWhenScrollingOnWideScreen() {
   	var sidebar = $('#ac-sidebar');
   	if($(window).width() > 1200) {		
		sidebar.css("width", "28%")
		var topOfSidebar = sidebar.offset().top - parseFloat(sidebar.css('margin-top'));

		$(window).scroll(function (event) {
	      var y = $(this).scrollTop();
          var scrollBelowTopOfSidebar = (y >= topOfSidebar);
          if (scrollBelowTopOfSidebar) {
	        sidebar.css("position", "fixed");
	        sidebar.css("top",  0);
            sidebar.css("width", "22.5%")
	      } else {
	        sidebar.css("position", "static");
            sidebar.css("width", "28%");
	      }
		});			
	}
	else {
		sidebar.css("position", "static");
		sidebar.css("width", "100%");
		$(window).off('scroll');
	}
   }

   fixSidebarWhenScrollingOnWideScreen();

   $(window).resize(function() {
   	fixSidebarWhenScrollingOnWideScreen();
   });

});