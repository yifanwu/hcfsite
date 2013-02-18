$(document).ready(function() {
    $('#person_bio').stickyfloat({duration: 0, offsetY: 10});

    $('.detail_box').click(function() {
    	img_src = $(this).children('img').attr('src');
    	name = $(this).find('.name').html();
    	title = $(this).find('.title').html();
    	organization = $(this).find('.organization').html();
        email = $(this).find('.email').html();
    	bio = $(this).find('.bio').html();

		var html ="<div class='person_descrip'><img src='" + img_src + "' alt='person pic'/>";
		html += "<span class='name'>" + name + "</span> <span class='title'>" + title + "</span><br/>";
        if (organization != undefined)
            html += "<span class='organization'>" + organization + "</span></br>";
        html += "<div class='cleaner'>&nbsp;</div></div>";
		html += "<p class='bio'>" + bio;
        if (email != undefined)
            html += "<br/><br/><br/>" + name + " may be reached at <a href='mailto:" + email + "'>" + email + "</a>.";
        html += "</p>";
		$('#person_bio').fadeOut(function() {
		    $(this).html(html).fadeIn();
		});
    });
});