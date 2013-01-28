$(document).ready(function() {
    $('.heading').click(function() {
	if ($(this).children('i').attr('class') == 'icon-chevron-down') {
	    $(this).parent().children('.descrip').slideDown();
	    $(this).children('i').attr('class', 'icon-chevron-up');
	} else {
	    $(this).parent().children('.descrip').slideUp();
	    $(this).children('i').attr('class', 'icon-chevron-down');
	}
    });
});
