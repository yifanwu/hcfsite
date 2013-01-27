$(document).ready(function() {
    $('.carousel').carousel({
	interval: 8000
    });

    $('.detail_box').click(function() {
	$('#modal').modal();
    });

    $('#panels_nav > li').click(function() {
	$('#panels_nav > li').removeClass('active');
	$(this).addClass('active');
    });
});
