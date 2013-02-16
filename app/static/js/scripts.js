$(document).ready(function() {
    $('#site_register').mouseover(function() {
	$('#site_register_top').slideDown('fast');
    });

    $('#site_register').mouseleave(function() {
	$('#site_register_top').slideUp('fast');
    });
    
    $(".scroll_to_anchor").click(function(event){		
	event.preventDefault();
	$('html,body').animate({scrollTop:$(this.hash).offset().top - 10}, 500);
    });
});