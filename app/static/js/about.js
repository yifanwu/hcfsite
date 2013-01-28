$(document).ready(function() {
    $('[data-spy="scroll"]').each(function () {
	var $spy = $(this).scrollspy('refresh')
    });
    $('#about_nav').on('activate', function (e) {
	$('#about_site_nav').addClass("active");
    })

    $('#about_nav_wrapper').css("height", $('#about').height() + "px");

    $('#about_nav').stickyfloat({duration: 0, offsetY: 10});
});
