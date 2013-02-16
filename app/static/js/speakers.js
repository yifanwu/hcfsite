$(document).ready(function() {
    $('.panel_select').click(function() {
		var panel = $(this).attr('id');

		$('.nav-pills > li').removeClass('active');
		$(this).parent().parent().parent().addClass('active');
		$('.panel_detail').fadeOut(300, function() {
	    		setTimeout(function() { $("." + panel).slideDown(200); }, 300);
		});
    });

    $('.nav-pills > li:first > ul > li:first > a').click();
});