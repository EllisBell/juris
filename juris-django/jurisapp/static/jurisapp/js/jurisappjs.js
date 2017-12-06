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

    // this adds event to buttons loaded through ajax call
    $(document).on("click", '#nextBtn', function(event) {
        query = $(this).data("query");
        alert(query);
    });

});