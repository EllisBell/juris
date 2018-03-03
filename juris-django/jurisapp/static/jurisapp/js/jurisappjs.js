$(document).ready(function() {

	//search...
	$('#searchbox').keydown(function(event) {
	//var code = event.
		if(event.keyCode == 13) {
			event.preventDefault();

			var query = $(this).val();
			var tribs = getCheckedTribs();			
			
			if(!query || tribs.length==0) {
				return;
			}

			showLoadingBar();

		 	$.get('/jurisapp/search/', {query: query, tribs: tribs}, function(data) {
				$(".loading").css("visibility", "hidden");
				$('#searchResults').html(data);
			});
		}
	});

	function getCheckedTribs() {
		var tribs = []
		$(".tribCheck").each(function() {
			if($(this).prop("checked")) {
				tribs.push($(this).data("trib"));
			}
		});
		return tribs;
	}

    // this adds event to buttons loaded through ajax call
    $(document).on("click", '.pageBtn', function(event) {
        var query = $(this).data("query");
        var page = $(this).data("page");
        // Get array of tribs as string and parse into array. Tribs passed from server so this search uses same set of tribs,
        // rather than the ones currently checked (which may have changed)
        // Comes from server as single quoted values so replace with double quotes for JSON parse to work
        var tribs = $(this).data("tribs");
        tribs = JSON.parse(tribs.replace(/'/g, "\""));

        // TODO look into improving pagination/search results UX e.g. when to clear, where to focus, progress bar etc.
        $(window).scrollTop(0);
 		showLoadingBar();

        $.get('/jurisapp/search/', {query: query, tribs: tribs, page: page}, function(data) {
				$(".loading").css("visibility", "hidden");
				$('#searchResults').html(data);
		 });
    });

    function showLoadingBar() {
            $('#searchResults').html("")
 		$(".loading").css("visibility", "visible");
    }

    // Changing checkbox/label colour when checked/unchecked
    $("input[type='checkbox']").change(function() {
    	var chkBox = $(this);
     	var label = $(this).parent();

    	if(chkBox.is(':checked')) {
    		label.css("background-color", "#9ff8cd");
    	}
    	else {
    		label.css("background-color", "#e3e5e4");
    	}
    });

    $(".orderByButton").click(function(event) {
    	// TODO search by relevance / sort
    	setOrderByButtonSelectedAndColours($(this));
    }); 


    function setOrderByButtonSelectedAndColours(selected) {
     	var selectedId = selected.attr('id')

    	$(".orderByButton").each(function(index) {
    		button = $(this);
    		buttonId = button.attr('id');
    		if(buttonId === selectedId) {
    			button.data("selected", true);
    			button.css("background-color", "#9ff8cd");
    		}
    		if(buttonId != selectedId) {
    			button.data("selected", false);
    			button.css("background-color", "#e3e5e4");
    		}
    	});
    }

    setOrderByButtonSelectedAndColours($("#relevanceBtn"));


});