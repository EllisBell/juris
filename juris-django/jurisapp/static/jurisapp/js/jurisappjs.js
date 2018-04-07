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

            handle_search_focus();
			showLoadingBar();
            setOrderByButtonSelectedAndColours($("#relevanceBtn"));
            getRelevant(query, tribs, 1);
		}
	});

	function getCheckedTribs() {
		var tribs = []
		$(".tribLabel").each(function() {
			if($(this).data("selected")) {
				tribs.push($(this).data("trib"));
			}
		});
		return tribs;
	}

    function handle_search_focus() {
        var mq = window.matchMedia("(max-width: 524px)");
        if(mq.matches) {
            $("#searchbox").blur();
        }
    }

	function showOrderByButtons() {
		if($("#currentSearch").data("total") > 0) {
            $("#orderByButtons").css("visibility", "visible");
        }
        else {
            $("#orderByButtons").css("visibility", "hidden");   
        }
	}

    // this adds event to buttons loaded through ajax call
    $(document).on("click", '.pageBtn', function(event) {
        var searchData = getCurrentSearchData();
        var pageToGoTo = $(this).hasClass("prevBtn") ? searchData.page-1 : searchData.page+1;

        // TODO look into improving pagination/search results UX e.g. when to clear, where to focus, progress bar etc.
        if($(this).hasClass("bottomPageBtn")) {
            $(window).scrollTop(0);
        }
 		showLoadingBar();
        if($("#relevanceBtn").data("selected")) {
            getRelevant(searchData.query, searchData.tribs, pageToGoTo);
        }
        else {
            getRecent(searchData.query, searchData.tribs, pageToGoTo);
        }
    });

    function getCurrentSearchData() {
        var query = $("#currentSearch").data("query");
        var page = $("#currentSearch").data("page");
        // Get array of tribs as string and parse into array. Tribs passed from server so this search uses same set of tribs,
        // rather than the ones currently checked (which may have changed)
        // Comes from server as single quoted values so replace with double quotes for JSON parse to work
        var tribs = $("#currentSearch").data("tribs");
        tribs = JSON.parse(tribs.replace(/'/g, "\""));

        var searchData = {
            query: query,
            page: page,
            tribs: tribs
        }
        return searchData;
    }


    function getRelevant(query, tribs, page) {
        // TODO this is sending date.now() as a way to get around IE caching results; bit of a hack, rework
         $.get('/search_relevant/', {"_": Date.now(), query: query, tribs: tribs, page: page}, function(data) {
                hideLoadingBar();
                $('#searchResults').html(data);
                $('#searchResults').css("visibility", "visible");
                showOrderByButtons();                
         });
    }

    function getRecent(query, tribs, page) {
        $.get('/search_recent/', {query: query, tribs: tribs, page: page}, function(data) {
                hideLoadingBar();
                $('#searchResults').html(data);
                $('#searchResults').css("visibility", "visible");
                showOrderByButtons();
        });
    }

    function showLoadingBar() {
        // TODO this is moving scroll bar up for some reason, fix
        var currentPos = $(window).scrollTop();
        $('#searchResults').css("visibility", "hidden");
        $('html,body').scrollTop(currentPos);
        $(".loading").css("display", "inline-block");
        }

    function hideLoadingBar() {
        $(".loading").css("display", "none");
    }

    // Changing checkbox/label colour when checked/unchecked
  /*  $("input[type='checkbox']").change(function() {
    	var chkBox = $(this);
     	var label = $(this).parent();

    	if(chkBox.is(':checked')) {
    		label.css("background-color", "#9ff8cd");
    	}
    	else {
    		label.css("background-color", "#e3e5e4");
    	}
    });*/

    $(".tribLabel").click(function(e) {
        var label = $(this);
        var currentlySelected = label.data("selected");
        if(!currentlySelected) {
            label.css("background-color", "#b4dce0");
            label.children(".ticked").css("display", "inline");
            label.children(".not-ticked").css("display", "none");
            label.data("selected", true);
        }
        else {
            label.css("background-color", "#e3e5e4");
            label.children(".ticked").css("display", "none");
            label.children(".not-ticked").css("display", "inline");           
            label.data("selected", false)
        }
    });

    function setTribLabel(label) {
        label.css("background-color", "#b4dce0");
        label.children(".ticked").css("display", "inline");
        label.children(".not-ticked").css("display", "none");
        label.data("selected", true);
    }

    $(".tribLabel").each(function(index) {
        setTribLabel($(this));
    });

    $(".orderByButton").click(function(event) {
    	currentlyRelevant = $("#relevanceBtn").data("selected");
        
        setOrderByButtonSelectedAndColours($(this));

        var searchData = getCurrentSearchData();

        if($("#relevanceBtn").data("selected") && !currentlyRelevant) {
            showLoadingBar();
            getRelevant(searchData.query, searchData.tribs, 1);
        }
        else if($("#recentBtn").data("selected") && currentlyRelevant) {
            showLoadingBar();
            getRecent(searchData.query, searchData.tribs, 1);
        }
    }); 


    function setOrderByButtonSelectedAndColours(selected) {
     	var selectedId = selected.attr('id')

    	$(".orderByButton").each(function(index) {
    		button = $(this);
    		buttonId = button.attr('id');
    		if(buttonId === selectedId) {
    			button.data("selected", true);
    			//button.css("background-color", "#9ff8cd");
                button.css("background-color", "#b4dce0");
            }
    		if(buttonId != selectedId) {
    			button.data("selected", false);
    			button.css("background-color", "#e3e5e4");
    		}
    	});
    }

    setOrderByButtonSelectedAndColours($("#relevanceBtn"));

});