$(document).ready(function() {

	//search...
	$('#searchbox').keydown(function(event) {
	//var code = event.
		if(event.keyCode == 13) {
			event.preventDefault();
			var query;
			query = $(this).val();
		 	$.get('/jurisapp/search/', {query: query}, function(data) {
				$('#searchResults').html(data);
			});
		}
	});

});