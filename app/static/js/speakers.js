$(document).ready(function() {
    $('.panel_select').click(function() {
	var panel = $(this).attr('id').substring(0, 9);
	var topic_id = $(this).attr('id').substring(10);
	var panel_title = "";

	switch(panel) {
	    case 'cult_soci': panel_title = "Culture/Society"; break;
	    case 'busi_inno': panel_title = "Business/Innovation"; break;
	    case 'econ_fina': panel_title = "Economics/Finance"; break;
	    default: return false;
	}

	switch(topic_id) {
	    case "1": panel_title += " I:<br/>Lorem Ipsum Dolor sit Amet Consectetur"; break;
	    case "2": panel_title += " II:<br/>Adipiscing Elit nunc Nec Magna sed Augue"; break;
	    case "3": panel_title += " III:<br/>Viverra Lacinia eu Sed em Class Aptent"; break;
	    case "4": panel_title += " IV:<br/>Aciti Sociosqu ad Litora"; break;
	    default: return false;
	}

	$('.nav-pills > li').removeClass('active');
	$('#' + panel).parent().addClass('active');
	$('#panel_detail').fadeOut(200, function() {
	    $('#panel_heading > h4').html(panel_title);
	    $(this).slideDown();
	});
    });

    $('#view_all').click(function() {
	$('.nav-pills').css("visibility", "hidden");
	$('#view_all').hide();
	$('#collapse').show();
	$('#people_more').hide();
	$('#people_more').html("<p><br/><br/>More panels go here... hehe.</p>");
	$('#people_more').slideDown();
    });

    $('#collapse').click(function() {
	$('#collapse').hide();
	$('#view_all').show();
	$('.nav-pills').css("visibility", "visible");
	$('#people_more').slideUp();
    });
});
