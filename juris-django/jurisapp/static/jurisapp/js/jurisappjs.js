$(document).ready(function() {

	//search...
	$('#searchbox').keydown(function(event) {
	//var code = event.
		if(event.keyCode == 13) {
			event.preventDefault();			
			
            var sd = getFreshSearchData();

            // TODO write isValidSearch method
			if(!sd.query || sd.tribs.length==0) {
				return;
			}

            handle_search_focus();
			showLoadingBar();
            setOrderByButtonSelectedAndColours($("#relevanceBtn"));
            getRelevant(sd);
            save_search(sd.query);
		}
	});

    function getFreshSearchData() {
        var query = $('#searchbox').val();
        var tribs = getCheckedTribs();
        var processo = $('#procSearch').val();
        var fromDate = getDateValue($('#fromDate'));
        var toDate = getDateValue($('#toDate'));
        var page = 1;

        return getSearchDataObj(query, tribs, processo, fromDate, toDate, page);  
    }

    // adding this function in case i wanna do some date formatting or something at some point
    function getDateValue(element) {
        return element.val();
    }

    function getSimpleFromDate() {
        var fromDate = $('#fromDate').val();
        return fromDate;
    }

    function getSimpleFromDate() {
        var fromDate = $('#fromDate').val();
        return fromDate;
    }

    function getFromDateAsDate() {
        var fromDate = $('#fromDate').val();
        return parseDate(fromDate);
    }

    function parseDate(dateString) {
        var parsedDate = $.datepicker.parseDate("dd/mm/yy", dateString);
        return parsedDate;
    }

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
        searchData.page = pageToGoTo;

        // TODO look into improving pagination/search results UX e.g. when to clear, where to focus, progress bar etc.
        if($(this).hasClass("bottomPageBtn")) {
            $(window).scrollTop(0);
        }
 		showLoadingBar();
        if($("#relevanceBtn").data("selected")) {
            getRelevant(searchData);
        }
        else {
            getRecent(searchData);
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

        var processo = $("#currentSearch").data("processo");; // todo get processo (have to add to currentsearch div)
        var firstDate = $("#currentSearch").data("from-date");; // todo get date
        var secondDate = $("#currentSearch").data("to-date");; // todo get date

        return getSearchDataObj(query, tribs, processo, firstDate, secondDate, page)
    }

    function getSearchDataObj(query, tribs, processo, fromDate, toDate, page) {
        var searchData = {
            query: query,
            tribs: tribs,
            processo: processo,
            fromDate: fromDate,
            toDate: toDate,
            page: page
        }
        return searchData;
    }

    function getRelevant(searchData) {
        // TODO this is sending date.now() as a way to get around IE caching results; bit of a hack, rework
         searchData._ = Date.now();
         $.get('/search_relevant/', 
                // data to go with request
                //{"_": Date.now(), query: searchData.query, tribs: searchData.tribs, page: searchData.page}, 
                searchData, 
                // callback function
                function(data) { displaySearchResults(data); }
            );
    }

    function getRecent(searchData) {
        $.get('/search_recent/', 
                searchData, 
                function(data) { displaySearchResults(data); }
        );
    }

    function displaySearchResults(searchResData) {
        hideLoadingBar();
        $('#searchResults').html(searchResData);
        $('#searchResults').css("visibility", "visible");
        showOrderByButtons();
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

    function save_search(query) {
        $.get('/save_search/', {query: query});
    }

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
            getRelevant(searchData);
        }
        else if($("#recentBtn").data("selected") && currentlyRelevant) {
            showLoadingBar();
            getRecent(searchData);
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

    /*var location_input=$('input[id="autocomplete-processo"]');
    location_input.autocomplete({
        source: "('/suggest_processo/'",
        minLength: 4
        });*/

    $(function() {
        $("#procSearch").autocomplete({
            source: "/suggest_processo/",
            minLength: 5,
        });
    });

    $(function() {
        $(".datePicker").datepicker(
            // configure datepicker
            { dateFormat: "dd/mm/yy",
                dayNamesMin: ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab"],
                monthNames: [ "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", 
                            "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro" ],
                changeYear: true,
                yearRange: "1932:" + new Date().getFullYear()
            }
        );
    });

  /*  $("#procSearch").bind("paste", function () {
        setTimeout(function () {
        $("#procSearch").autocomplete("search", $("#procSearch").val());
        }, 0);
    });*/

    //   keeps same width as box
    /*  jQuery.ui.autocomplete.prototype._resizeMenu = function () {
          var ul = this.menu.element;
          ul.outerWidth(this.element.outerWidth());
    }*/

});

      jQuery.ui.autocomplete.prototype._resizeMenu = function () {
          var ul = this.menu.element;
          ul.outerWidth(this.element.outerWidth());
        }