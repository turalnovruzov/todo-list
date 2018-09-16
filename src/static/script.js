$(document).ready(function () {
    $.validator.addMethod("usernameCheck", function(value, element){
        let return_value = true;
        $.ajax({
            type: "POST",
            url: "/api/username_check",
            data: { username: value },
            success: (data) => {
                return_value = !data.exists;
            },
            async: false
          });
        console.log(return_value);
        return return_value;
    }, "Username is already taken."); 

    $("#signup-form").validate({
        rules: {
            username: {
                required: true,
                usernameCheck: true
            },
            password: {
                required: true,
                minlength: 5
            },
            confirmation: {
                required: true,
                equalTo: "#password"
            }
        },
        messages: {
            password: {
                minlength: "Password must be at least 5 characters long."
            },
            confirmation: {
                equalTo: "Passwords don't match."
            }
        },
        errorElement: "div",
        errorPlacement: (error, element) => {
            $(error).addClass("invalid-feedback");
            $(error).insertAfter(element);
        },
        highlight: (element, errorClass, validClass) => {
            $(element).addClass("is-invalid").removeClass("is-valid");
        },
        unhighlight: (element, errorClass, validClass) => {
            $(element).addClass("is-valid").removeClass("is-invalid");
        }
    });
});