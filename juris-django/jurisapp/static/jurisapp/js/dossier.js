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
        $("#folder-name-input-area").focus();
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

    $("#edit-folder-description").click(function() {
        $("#folder-description").addClass("is-hidden");
        $("#folder-description-input-area").removeClass("is-hidden");
        $("#folder-description-input-area").focus();
        $("#edit-folder-description").addClass("is-hidden");
        $("#confirm-folder-description").removeClass("is-hidden");
      });

    $("#confirm-folder-description").click(function() {
        var newDescription = $("#folder-description-input").val();
        $("#folder-description").removeClass("is-hidden");
        $("#folder-description").text(newDescription);
        $("#folder-description-input-area").addClass("is-hidden");
        $("#confirm-folder-description").addClass("is-hidden");
        $("#edit-folder-description").removeClass("is-hidden");

        editFolder();
    });

    function editFolder() {
        var id = $("#folder-id").val();
        var newName = $("#folder-name-input").val();
        var newDescription = $("#folder-description-input").val();
        
        $.post('/edit-folder/',
        {
            folder_id: id,
            folder_name: newName,
            folder_description: newDescription
        },
        function(data) {}
        )
    }

    $(".archive-folder-btn").click(function(e){
        var folderId = $(e.target).data("folder-id");
        $("#archive-folder-modal").addClass("is-active");
        $("#archive-folder-id").val(folderId);
    });

    $(".close-archive-modal").click(function(){
        hideArchiveFolderModal();
    });

    function hideArchiveFolderModal() {
        $("#archive-folder-modal").removeClass("is-active");
    }

    $("#confirm-archive-folder").click(function(){
        var folderId = $("#archive-folder-id").val();
        $.post('/archive-folder/',
                {folder_id: folderId},
                function(data) {
                    var archived = $("#folder-box-" + folderId);
                    archived.addClass("is-hidden");
                    hideArchiveFolderModal();
                }
              )
    });

    $(".unarchive-folder-btn").click(function(e){
        var folderId = $(e.target).data("folder-id");
        $.post('/unarchive-folder/',
        {folder_id: folderId},
        function(data) {
            var unarchived = $("#folder-box-" + folderId);
            unarchived.addClass("is-hidden");
        }
      );
    });

    // Remove acordao from dossier

    $(".remove-acordao-btn").click(function(e){
        var acordaoId = $(e.target).data("acordao-id");
        $("#remove-acordao-modal").addClass("is-active");
        $("#remove-acordao-id").val(acordaoId);
    });

    $(".close-remove-acordao-modal").click(function(){
        hideRemoveAcordaoModal();
    });

    function hideRemoveAcordaoModal() {
        $("#remove-acordao-modal").removeClass("is-active");
    }

    $("#confirm-remove-acordao").click(function(){
        var acordaoId = $("#remove-acordao-id").val();
        var folderId = $("#folder-id").val();
        $.post('/remove-acordao/',
                {
                    folder_id: folderId, 
                    acordao_id: acordaoId
                },
                function(data) {
                    var removed = $("#acordao-box-" + acordaoId);
                    removed.addClass("is-hidden");
                    hideRemoveAcordaoModal();
                }
              )
    });

});