$(document).ready(function() {
    $('[data-spy="scroll"]').each(function () {
	var $spy = $(this).scrollspy('refresh')
    });
    $('#panels_nav').on('activate', function (e) {
	$('#panels_site_nav').addClass("active");
    })

    $('#panels_nav_wrapper').css("height", $('#panels').height() + "px");

    $('#panels_nav').stickyfloat({duration: 0, offsetY: 10});
});
