$(document).ready(function() {

	//search...
	$('#searchbox').keypress(function(e) {
	//var code = event.
		if(e.keyCode == 13) {
			e.preventDefault();			
            doFreshSearch();
		}
	});

    function isNumber(input) {
        return !isNaN(parseInt(input));
    }

   $(".searchBtn").click(function() {
        doFreshSearch();
    });

   $(".showAdv").click(function() {
    var adv = $("#advancedSearch");
    if(adv.is(':visible')) {
        adv.hide(200);
        clearAdvancedSearch();
    }
    else {
        adv.show(200);
    }
    });

    $("#procSearch").autocomplete({
        source: "/suggest_processo/",
        minLength: 4,
    });

    $("#procSearch").keydown(function(event) {
        if(event.keyCode == 13) {
            event.preventDefault();
            doFreshSearch();
        }
    });

    $("#searchbox").autocomplete({
        //source: "/suggest_processo/",
        source: function (request, response) {
            // full string
            //var term = request.term;
            var currentlyTypedWord = getCurrentlyTypedWord($("#searchbox").get(0)).word;
            jQuery.get("/suggest_processo/", 
                {term: currentlyTypedWord}, 
                function (data) {
                // Add "Proc nº" for context
                for(var i=0; i<data.length; i++) {
                    data[i].label = "Proc. nº " + data[i].label;
                }
                response(data);
            });
        },
        minLength: 4,
        search: function(event, ui) {
            // Only trigger autocomplete if word being typed starts with number
            var currentlyTypedWord = getCurrentlyTypedWord(event.target).word;
            return isAutoCompleteable(currentlyTypedWord);
        },
        focus: function(event, ui) {
            // when scrolling through autocomplete options do not replace text with option
            event.preventDefault();
        },
        select: function (event, ui) {
            // When option selected, replace search term within string with selected option
            var fullText = $("#searchbox").val();
            var info = getCurrentlyTypedWord($("#searchbox").get(0));
            var beforeTerm = fullText.substr(0, info.startInd);
            var afterTerm = fullText.substr(info.endInd+1);
            var newText = beforeTerm + ui.item.value + afterTerm;
            $("#searchbox").val(newText);
            return false;
        },             
    }).keyup(function(e) {
            // hide autocomplete options dropdown on spacebar
            if(e.keyCode == 32) {
                $(".ui-menu-item").hide(); 
            }
            // on arrow keys or backspace, if moved to non searchable word, hide dropdown
            else if(e.keyCode == 39 || e.keyCode == 37 || e.keyCode == 8) {
                var currentlyTypedWord = getCurrentlyTypedWord($("#searchbox").get(0)).word;
                if(!isAutoCompleteable(currentlyTypedWord)) {
                    $(".ui-menu-item").hide(); 
                }
            }
    }); 

    function isAutoCompleteable(word) {
        return firstCharIsNumber(word) && word.length >= 4
    }

    function firstCharIsNumber(word) {
        return isNumber(word.substr(0,1));
    }

    function getCurrentlyTypedWord(element) {
        var text = element.value;
        var caretPosition = doGetCaretPosition(element);
        // find last space up to here
        var stringUpToCaret = text.substr(0, caretPosition);
        // if spacebefore not found, will return -1, in which case start will be 0
        var spaceBefore = stringUpToCaret.lastIndexOf(" ");
        var startOfCurrentlyTyped = spaceBefore + 1;

        var stringAfterCaret = text.substr(caretPosition);
        var spaceAfter = stringAfterCaret.indexOf(" ");
        var endOfCurrentlyTyped;
        if(spaceAfter != -1) {
            endOfCurrentlyTyped = stringUpToCaret.length + spaceAfter - 1;
        }
        else {
            endOfCurrentlyTyped = text.length;
        }

        // substring(start index, length of substring)
        var currentlyTypedWord = text.substr(startOfCurrentlyTyped, (endOfCurrentlyTyped-startOfCurrentlyTyped)+1);

        var currentlyTypedWordInfo = {
            word: currentlyTypedWord,
            startInd: startOfCurrentlyTyped,
            endInd: endOfCurrentlyTyped
        }
        return currentlyTypedWordInfo;
    }

    function setCursorEndOfTextInput(elem) {
        text = elem.val();
        elem.focus();
        elem.val('');
        elem.val(text);
    }

    function doGetCaretPosition (oField) {

          // Initialize
          var iCaretPos = 0;

          // IE Support
          if (document.selection) {

            // Set focus on the element
            oField.focus();

            // To get cursor position, get empty selection range
            var oSel = document.selection.createRange();

            // Move selection start to 0 position
            oSel.moveStart('character', -oField.value.length);

            // The caret position is selection length
            iCaretPos = oSel.text.length;
          }

          // Firefox support
          else if (oField.selectionStart || oField.selectionStart == '0')
            iCaretPos = oField.selectionStart;

          // Return results
          return iCaretPos;
    }

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

    $(".datePicker").keyup(function(e) {
    if(e.keyCode == 8 || e.keyCode == 46) {
        $.datepicker._clearDate($(this));
    }
    });

    $("#clearFromDate").click(function(e) {
        $("#fromDate").datepicker("setDate", null);
        $("#toDate").datepicker("setDate", null);
        $(".dateClear").css("visibility", "hidden");
    });

    $("#clearToDate").click(function(e) {
        $("#toDate").datepicker("setDate", null);
        $("#clearToDate").css("visibility", "hidden");
    });

    $("#fromDate").datepicker("option", "onSelect", function(dateText) { 
        // TODO check if todate is null or before new from date, if it is, change it to new from date otherwise leave as is
        $("#clearFromDate").css("visibility", "visible");
        var newFromDate = $(this).datepicker("getDate");
        var currentToDate = $("#toDate").datepicker("getDate");
        if(currentToDate && currentToDate < newFromDate) {
            $("#toDate").datepicker("setDate", dateText);
            $("#clearToDate").css("visibility", "visible");
        }
        $("#toDate").datepicker("option", "minDate", newFromDate);
    }); 

    $("#toDate").datepicker("option", "onSelect", function(dateText) {  
        $("#clearToDate").css("visibility", "visible");
        var currentFromDate = $("#fromDate").datepicker("getDate");
        if(!currentFromDate) {
            $("#fromDate").datepicker("setDate", dateText);
            $("#clearFromDate").css("visibility", "visible");
        }
    }); 

    function clearAdvancedSearch() {
        $("#procSearch").val("")
        $("#fromDate").datepicker("setDate", null);
        $("#toDate").datepicker("setDate", null);
    }

    function doFreshSearch() {
         var sd = getFreshSearchData();

        var validSearch = isValidSearch(sd);

        if(!validSearch) {
            return;
        }

        handle_search_focus();
        showLoadingBar();
        setOrderByButtonSelectedAndColours($("#relevanceBtn"));
        getRelevant(sd);
        save_search(sd.query);
    }

    function getFreshSearchData() {
        var query = $('#searchbox').val();
        var tribs = getCheckedTribs();
        var processo = $('#procSearch').val();
        var fromDate = getDateValue($('#fromDate'));
        var toDate = getDateValue($('#toDate'));
        var page = 1;
        var justTxtIntegral = getJustTxtIntegralValue();

        return getSearchDataObj(query, tribs, processo, fromDate, toDate, page, justTxtIntegral);  
    }

    function getJustTxtIntegralValue() {
        var checkbox = $("#justTxtIntegralCheck");
        //return checkbox.prop('checked');
        return checkbox.data("selected");
    }

    // adding this function in case i wanna do some date formatting or something at some point
    function getDateValue(element) {
        return element.val();
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
    function isValidSearch(sd) {
        // todo if any of the things are there AND there is at least one trib selected, search
        return (sd.query || sd.processo || sd.fromDate) && sd.tribs.length > 0
    }


    function handle_search_focus() {
        var mq = window.matchMedia("(max-width: 524px)");
        if(mq.matches) {
            $("#searchbox").blur();
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

        var justTxtIntegral = getJustTxtIntegralValue();

        return getSearchDataObj(query, tribs, processo, firstDate, secondDate, page, justTxtIntegral)    
    }

    function getSearchDataObj(query, tribs, processo, fromDate, toDate, page, justTxtIntegral) {
        var searchData = {
            query: query,
            tribs: tribs,
            processo: processo,
            fromDate: fromDate,
            toDate: toDate,
            page: page,
            justTxtIntegral: justTxtIntegral
        }
        return searchData;
    }

    function getRelevant(searchData) {
        // TODO this is sending date.now() as a way to get around IE caching results; bit of a hack, rework
         searchData._ = Date.now();
         $.get('/search_relevant/', 
                // data to go with request
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
        $(".loading").css("display", "block");
        }

    function hideLoadingBar() {
        $(".loading").css("display", "none");
    }

    function showOrderByButtons() {
        if($("#currentSearch").data("total") > 0) {
            $("#orderByButtons").css("visibility", "visible");
        }
        else {
            $("#orderByButtons").css("visibility", "hidden");   
        }
    }

    function save_search(query) {
        $.get('/save_search/', {query: query});
    }

    $(".tribLabel").click(function(e) {
        var label = $(this);
        var currentlySelected = label.data("selected");
        if(!currentlySelected) {
            label.children(".ticked").css("display", "inline");
            label.children(".not-ticked").css("display", "none");
            label.data("selected", true);
        }
        else {
            label.children(".ticked").css("display", "none");
            label.children(".not-ticked").css("display", "inline");           
            label.data("selected", false)
        }
    });

    function setTribLabel(label) {
        label.children(".ticked").css("display", "inline");
        label.children(".not-ticked").css("display", "none");
        label.data("selected", true);
    }

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

    $("#justTxtIntegralCheck").click(function(event) {
        var check = $(this);
        var currentlySelected = getJustTxtIntegralValue();

        if(currentlySelected) {
            check.children(".ticked").css("display", "none");
            check.children(".not-ticked").css("display", "inline");    
        }
        else {
            check.children(".ticked").css("display", "inline");
            check.children(".not-ticked").css("display", "none"); 
        }

        check.data("selected", !currentlySelected);

        var searchData = getCurrentSearchData();
        showLoadingBar();
        if(relevantIsSelected()) {
            getRelevant(searchData);
        }
        else {
            console.log("relevant not selected");
            getRecent(searchData);
        }
    });

    function relevantIsSelected() {
        console.log($("#relevanceBtn").data("selected"));
        return $("#relevanceBtn").data("selected");
    }

    function recentIsSelected() {
        return $("#recentBtn").data("selected");
    }


    function setOrderByButtonSelectedAndColours(selected) {
     	var selectedId = selected.attr('id')

    	$(".orderByButton").each(function(index) {
    		button = $(this);
    		buttonId = button.attr('id');
    		if(buttonId === selectedId) {
    			button.data("selected", true);
                 button.addClass("is-outlined");
            }
    		if(buttonId != selectedId) {
                button.data("selected", false);
                button.removeClass("is-outlined");
    		}
    	});
    }

    setOrderByButtonSelectedAndColours($("#relevanceBtn"));


    jQuery.ui.autocomplete.prototype._resizeMenu = function () {
        var ul = this.menu.element;
        ul.outerWidth(this.element.outerWidth());
    }

});

