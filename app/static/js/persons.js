$(document).ready(function() {
    $('#person_bio').stickyfloat({duration: 0, offsetY: 10});

    $('.detail_box').click(function() {
	var speaker_id = $(this).attr('id');
	var html ="<div class='person_descrip'><img src='img/people/icons/" + speaker_id  + ".jpg' alt='person pic'/>";
	html += "<span class='name'>Person Name</span> <span class='title'>Person Title<br/>Person Organization</br></span><div class='cleaner'>&nbsp;</div></div>";
	html += "<p class='bio'>In pharetra justo mollis purus vestibulum ac consectetur nisl gravida. In hac habitasse platea dictumst. Curabitur fringilla eros eget risus scelerisque sed pharetra urna auctor. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Quisque malesuada imperdiet ipsum, id pharetra eros semper sed. Quisque accumsan quam sed dolor pretium vel interdum nibh blandit.</p>";
	$('#person_bio').fadeOut(function() {
	    $(this).html(html).fadeIn();
	});
    });
});
