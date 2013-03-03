$(document).ready(function() {
    $('.panel_select').click(function() {
	var panel = $(this).attr('id');
	
	$('.nav-pills > li').removeClass('active');
	// hack for keynote speakers
	if ($(this).html() == "Keynote")
	    $(this).parent().addClass('active');
	else
	    $(this).parent().parent().parent().addClass('active');
	$('.panel_detail').fadeOut(300, function() {
	    setTimeout(function() { $("." + panel).slideDown(200); }, 300);
	});
    });

    $('.nav-pills > li:first >  a').click();
});
