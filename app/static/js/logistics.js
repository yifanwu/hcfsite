$(document).ready(function() {
    $('[data-spy="scroll"]').each(function () {
	var $spy = $(this).scrollspy('refresh')
    });
    $('#logistics_nav').on('activate', function (e) {
	$('#logistics_site_nav').addClass("active");
    })

    $('#logistics_nav_wrapper').css("height", $('#logistics').height() + "px");

    $('#logistics_nav').stickyfloat({duration: 0, offsetY: 10});
});
