$(document).ready(function() {

	/****************** acordao page **********************/

	// Prevent form submission on enter
	$(window).keydown(function(event){
		if(event.keyCode == 13) {
		  event.preventDefault();
		  return false;
		}
	  });
	
	$(".save-acordao-modal-btn").click(function() {
		$("#save-acordao-modal").toggleClass("is-active");
   	});

   $(document).click(function(e) {
		var clickWasOpenButton = e.target.id === "save-acordao-modal-open-btn"
		if ($(e.target).closest('#save-acordao-modal-card').length === 0 && !clickWasOpenButton) {
			$('#save-acordao-modal').removeClass('is-active');
		}
	});

	$("#folder-name-textbox").keyup(function(e) {
		var newName = $("#folder-name-textbox").val();
		setChosenFolderName(newName, true);
		setChosenFolderId(null);
		setFolderNameField(newName);
		removeExistingFolderOutlines();
	});

	// $("#save-in-new-folder-btn").click(function(e) {
	// 	removeExistingFolderOutlines();
	// 	var name = $("#new-folder-name-input").val();
	// 	setChosenFolderName(name, true);
	// });

	$(".existing-folder").click(function(e) {
		removeExistingFolderOutlines();
		var folderId = $(this).data("id");
		setChosenFolderId(folderId);
		$(this).css("border", "1px solid green");
		var name = $(this).data("name");
		setChosenFolderName(name, false);
		setFolderNameField(name);
	});

	function removeExistingFolderOutlines() {
		$(".existing-folder").css("border", "none");
	}

	function setFolderNameField(folderName) {
		$("#new-folder-name-input").val(folderName);
	}

	function setChosenFolderName(name, isNew) {
		if(name.length > 0) {
			var extra = isNew ? ' (dossier novo)' : '';
			$("#save-acordao-folder-name").text(name + extra);
			$("#save-acordao-submit-btn").prop('disabled', false);
		}
		else {
			$("#save-acordao-folder-name").text("(crie ou escolha um dossier)");
			$("#save-acordao-submit-btn").prop('disabled', true);
		}
		//$("#new-folder-name-input").val(name)
	}

	function setChosenFolderId(folderId) {
		$("#save-acordao-dossier-id").val(folderId)
	}

	$(".notification-close-btn").click(function(e) {
		$(".notification").addClass("is-hidden");
	})

	// this is the id of the form
	$("#save-acordao-form").submit(function(e) {
		e.preventDefault(); // avoid to execute the actual submit of the form.

		var form = $(this);
		//var url = form.attr('action');

		$.ajax({
			type: "POST",
			url: "/guardar-acordao/",
			data: form.serialize(), // serializes the form's elements.
			success: function(data)
			{
				$('#save-acordao-modal').removeClass('is-active');
				$('#notification-dossier-name').text(data.folder_name);
				$('#saved-acordao-success-notification').removeClass('is-hidden');
			},
			error: function(data) 
			{
				$('#save-acordao-modal').removeClass('is-active');
				$('#saved-acordao-error-notification').removeClass('is-hidden');
			}
			});
			
	});
	

});