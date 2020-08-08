$(document).ready(function() {
    $("#dossier-search-input").keypress(function(e) {        
        if(e.keyCode == 13) {
            e.preventDefault();		
            dossierSearch();
		}
    });

    function dossierSearch() {
        var query = $("#dossier-search-input").val();

        if(!query) {
            backToDefault();
            return;
        }

       var dossier_id = $("dossier-id").val();


        searchData = {
            query: query,
            dossier_id: dossier_id
        };

        $.get('/dossier_search/',
                searchData,
                function(data) {displaySearchResults(data);})

    }

    function displaySearchResults(data) {
        $("#dossier-search-results").html(data);
        $("#dossier-normal-content").css("display", "none");
        $("#dossier-search-results").css("display", "block");
    }

    function backToDefault() {
        $("#dossier-normal-content").css("display", "block");
        $("#dossier-search-results").css("display", "none");
    }

    function setInitialTabDisplay() {
        
    }

    $('body').on('click', '#dossier-tabs li', function() {
        var tab = $(this).data('tab');
    
        $('#dossier-tabs li').removeClass('is-active');
        $(this).addClass('is-active');
    
        // $('.tab-content').css("display", "none")
        // $('.tab-content[data-content="' + tab + '"]').css('display', 'block');

        $('.tab-content').removeClass("is-active");
        $('.tab-content[data-content="' + tab + '"]').addClass("is-active");
      });
});