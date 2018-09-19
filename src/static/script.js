function reloadTodoList() {
    $.getJSON("/", { json: 1 },
        (data, textStatus, jqXHR) => {
            var todoItems = ""
            for(let i = 0; i < data.length; i++) {
                todoItems += `<div class="todo-item input-group">
                                  <span class="todo-item-caption form-control">${data[i].content}</span>
                                  <div class="input-group-append">
                                      <button class="btn btn-secondary todo-item-remove" type="button" id="${data[i].id}"><i class="fas fa-trash-alt"></i></button>
                                  </div>
                              </div>`
            }

            $("#todo-items-container").html(todoItems);
        }
    );
}

$(document).ready(function () {
    $.validator.addMethod("usernameCheck", (value, element) => {
        var return_value = true;
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

    $(document).on("click", ".todo-item-remove", function() {
        $.ajax({
            type: "DELETE",
            url: "/",
            data: {id: this.id},
            success: (response) => {
                reloadTodoList();
            }
        });

        return false;
    });

    $(document).on("submit", "#todo-add-form", function() {
        if ($("#todo-add-caption").val()) {
            $.ajax({
                type: "POST",
                url: "/",
                data: {content: $("#todo-add-caption").val()},
                success: (response) => {
                    reloadTodoList();
                }
            });
        }

        return false;
    });

    // $(document).on("hover", ".todo-item",
    //     (e) => {
    //         e.target.children().trigger("mouseenter");
    //     },
    //     (e) => {
    //         e.target.children().trigger("mouseleave");
    //     }
    // );
});