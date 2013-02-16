$(document).ready(function() {
    $('#site_register').mouseover(function() {
	$('#site_register_top').slideDown('fast');
    });

    $('#site_register').mouseleave(function() {
	$('#site_register_top').slideUp('fast');
    });

    $('#site_register').click(function() {
        window.location = "http://16th-harvardchinaforum.eventdove.com/";
    });

    $('.ribbon').click(function() {
        window.location = "http://16th-harvardchinaforum.eventdove.com/";
    });
    
    $(".scroll_to_anchor").click(function(event){		
	event.preventDefault();
	$('html,body').animate({scrollTop:$(this.hash).offset().top - 10}, 500);
    });
});