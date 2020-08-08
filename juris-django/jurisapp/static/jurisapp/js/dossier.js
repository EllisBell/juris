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
    
    // TODO temporary, move somewhere else
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    var csrftoken = getCookie('csrftoken');

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }


    $("#edit-folder-name").click(function() {
        $("#folder-name").addClass("is-hidden");
        $("#folder-name-input-area").removeClass("is-hidden");
        $("#edit-folder-name").addClass("is-hidden");
        $("#confirm-folder-name").removeClass("is-hidden");
      });

    $("#confirm-folder-name").click(function() {
        var newName = $("#folder-name-input").val();
        $("#folder-name").removeClass("is-hidden");
        $("#folder-name").text(newName);
        $("#folder-name-input-area").addClass("is-hidden");
        $("#confirm-folder-name").addClass("is-hidden");
        $("#edit-folder-name").removeClass("is-hidden");

        editFolder();
    });

    function editFolder() {
        var id = $("#folder-id").val();
        var newName = $("#folder-name-input").val();
        var newDescription = $("#folder-description").text();
        
        $.post('/edit-folder/',
        {
            folder_id: id,
            folder_name: newName,
            folder_description: newDescription
        },
        function(data) {}
        )
    }


});