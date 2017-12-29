$(document).ready(function() {

	//search...
	$('#searchbox').keydown(function(event) {
	//var code = event.
		if(event.keyCode == 13) {
			event.preventDefault();
			$('#searchResults').html("")
			$(".loading").css("visibility", "visible");
			var query;
			query = $(this).val();
		 	$.get('/jurisapp/search/', {query: query}, function(data) {
				$(".loading").css("visibility", "hidden");
				$('#searchResults').html(data);
			});
		}
	});

    // this adds event to buttons loaded through ajax call
    $(document).on("click", '.pageBtn', function(event) {
        query = $(this).data("query");
        page = $(this).data("page");
        // TODO look into improving pagination/search results UX e.g. when to clear, where to focus, progress bar etc.
        $(window).scrollTop(0);
        $('#searchResults').html("")
 		$(".loading").css("visibility", "visible");
        $.get('/jurisapp/search/', {query: query, page: page}, function(data) {
				$(".loading").css("visibility", "hidden");
				$('#searchResults').html(data);
		 });
    });


/*    loadResults = function(query, page) {
     $.get('/jurisapp/search/', {query: query, page: page}, function(data) {
				$('#searchResults').html(data);}
    }*/

    $(function () {
    var sidebar = $('#ac-sidebar');
    var top = sidebar.offset().top - parseFloat(sidebar.css('margin-top'));

    $(window).scroll(function (event) {
      var y = $(this).scrollTop();
      if (y >= top) {
        sidebar.css("position", "fixed");
        sidebar.css("top",  0);
      } else {
        sidebar.css("position", "static");
      }
    });
});

});