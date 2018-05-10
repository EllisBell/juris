$(document).ready(function() {

	//search...
	$('#searchbox').keyup(function(e) {
	//var code = event.
		if(e.keyCode == 13) {
			e.preventDefault();			
            doFreshSearch();
		}
        else {
           /* var text = $('#searchbox').val();
            var lastChar = text.substr(text.length-1);
            if(lastChar == 'y') {
                // remove last char, as we want to start textbox before it (to include it)
                var withoutLast = text.substr(0, text.length-1);
                var cheatWidth = getWidth(withoutLast);
                
                var target = $(e.target);
                var x = target.offset().left;
                var y = target.offset().top;
                x = x + cheatWidth;

                var procSearchExp = appendProcSearchExp(x, y);
                setUpTextForTypingInProcSearchExp(lastChar, withoutLast);
            }*/
            setUpMainSearchAutoComplete();
        }
	});

    function setUpMainSearchAutoComplete() {
        var searchBox = $("#searchbox");
        var text = searchBox.val();
        var tokens = text.split(" ");
        var lastToken = tokens[tokens.length-1];
        firstCharOfLastToken = lastToken.substr(0, 1);
        
        if(isNumber(firstCharOfLastToken) && lastToken.length > 3) {
            var withoutLast = text.substr(0, text.length-lastToken.length);
            var cheatWidth = getWidth(withoutLast);
            
            var x = searchBox.offset().left;
            var y = searchBox.offset().top;
            x = x + cheatWidth;

            var procSearchExp = appendProcSearchExp(x, y);
            setUpTextForTypingInProcSearchExp(lastToken, withoutLast);
        }
    }

    function isNumber(input) {
        return !isNaN(parseInt(input));
    }

    function getWidth(text) {
        $("#cheatDiv").text(text);
        var cheatWidth = $("#cheatDiv").width();
        return cheatWidth;
    }

    function appendProcSearchExp(x, y) {
        $("#content").append('<span contenteditable="true" id="procSearchExp"></span>');
        var procSearchExp = $("#procSearchExp");
        procSearchExp.css({"left": x + "px", "top": y + "px"});
        return procSearchExp;
    }

    function setUpTextForTypingInProcSearchExp(procSearchExpText, mainSearchText) {
        var procSearchExp = $("#procSearchExp")
        procSearchExp.focus();
        procSearchExp.text(procSearchExpText);
        setEndOfContenteditable(procSearchExp.get(0));
        $("#searchbox").val(mainSearchText);
    }

    function setEndOfContenteditable(contentEditableElement)
    {
        var range,selection;
        if(document.createRange)//Firefox, Chrome, Opera, Safari, IE 9+
        {
            range = document.createRange();//Create a range (a range is a like the selection but invisible)
            range.selectNodeContents(contentEditableElement);//Select the entire contents of the element with the range
            range.collapse(false);//collapse the range to the end point. false means collapse to end rather than the start
            selection = window.getSelection();//get the selection object (allows you to change selection)
            selection.removeAllRanges();//remove any selections already made
            selection.addRange(range);//make the range you have just created the visible selection
        }
        else if(document.selection)//IE 8 and lower
        { 
            range = document.body.createTextRange();//Create a range (a range is a like the selection but invisible)
            range.moveToElementText(contentEditableElement);//Select the entire contents of the element with the range
            range.collapse(false);//collapse the range to the end point. false means collapse to end rather than the start
            range.select();//Select the range (make it the visible selection
        }
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

    (function ($) {
        var original = $.fn.val;
        $.fn.val = function() {
        if ($(this).is('[contenteditable]')) {
            return $.fn.text.apply(this, arguments);
        };
        return original.apply(this, arguments);
        };
    })(jQuery);

    $(document).on('keydown.autocomplete', "#procSearchExp", function() {
        $(this).autocomplete({
                source: "/suggest_processo/",
                minLength: 4,
                select: function (event, ui) {        
                    var searchBox = $("#searchbox");
                    currentSearch = searchBox.val();
                    newSearch = currentSearch + ui.item.value;
                    $("#procSearchExp").remove();
                    searchBox.focus();
                    searchBox.val('');
                    searchBox.val(newSearch);
                    //alert(ui.item.label);
                    return false;
                },
        });
    });

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

        return getSearchDataObj(query, tribs, processo, fromDate, toDate, page);  
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

});

    jQuery.ui.autocomplete.prototype._resizeMenu = function () {
        var ul = this.menu.element;
        ul.outerWidth(this.element.outerWidth());
    }