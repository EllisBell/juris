$(document).ready(function() {

	$("#menu-icon").click(function(e) {
		$("#menu-div").css("display", "block");
		$("#menu-icon").css("display", "none");
		$("#menu-close").css("display", "block");
    });

    $("#menu-close").click(function(e) {
		$("#menu-div").css("display", "none");
		$("#menu-icon").css("display", "block");
		$("#menu-close").css("display", "none");

    });


});