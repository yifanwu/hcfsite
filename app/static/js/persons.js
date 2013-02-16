$(document).ready(function() {
    $('#person_bio').stickyfloat({duration: 0, offsetY: 10});

    $('.detail_box').click(function() {
    	img_src = $(this).children('img').attr('src')
    	console.log($(this).find('.name').html())
    	name = $(this).find('.name').html()
    	title = $(this).find('.title').html()
    	organization = $(this).find('.organization').html()
    	bio = $(this).find('.bio').html()

		var html ="<div class='person_descrip'><img src='" + img_src + "' alt='person pic'/>";
		html += "<span class='name'>" + name + "</span> <span class='title'>" + title + "<br/>" + organization + "</br></span><div class='cleaner'>&nbsp;</div></div>";
		html += "<p class='bio'>" + bio + "</p>";
		$('#person_bio').fadeOut(function() {
		    $(this).html(html).fadeIn();
		});
    });
});