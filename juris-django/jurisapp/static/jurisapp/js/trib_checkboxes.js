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