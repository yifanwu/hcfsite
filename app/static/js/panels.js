$(document).ready(function() {
    $('[data-spy="scroll"]').each(function () {
	var $spy = $(this).scrollspy('refresh')
    });
    $('#side_nav').on('activate', function (e) {
	$('#panels_site_nav').addClass("active");
    })

    $('#panels_nav_wrapper').css("height", $('#panels').height() + "px");

    $('#side_nav').stickyfloat({duration: 0, offsetY: 10});

    $('#side_nav > ul > li:first').addClass('active')
});
