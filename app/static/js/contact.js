$(document).ready(function(){
    // Validate form client-side before sending it to the server
    $("#contact").validate({
	rules:  {
	    subject: "required",
	    email: {
		required: true,
		email: true
	    },
	    message: "required"
	}
    });

    $('#reset').click(function() {
	$('label.error').remove();
    });
});
