function reset_password_handler () {

    $(document).on('click', '#change-to-reset-password-form', function () {
        $.ajax({
            url: 'reset-password-handler/',
            type: 'POST',
            data: {
                action: 'reset-password',
                csrfmiddlewaretoken: Cookies.get('csrftoken'),
            },
            success: function(response){
                $('#main-form').html(response)
            },
            error: function(){
                console.log('internal error.')
            },
        });
    })
}


function registration_handler () {

    $(document).on('click', '#change-to-registration-form', function () {
        $.ajax({
            url: 'registration-handler/',
            type: 'POST',
            data: {
                action: 'registration',
                csrfmiddlewaretoken: Cookies.get('csrftoken'),
            },
            success: function(response){
                $('#main-form').html(response)
            },
            error: function(){
                console.log('internal error.')
            },
        });
    })
}


function login_handler () {

    $(document).on('click', '#change-to-login-form', function () {
        $.ajax({
            url: 'login-handler/',
            type: 'POST',
            data: {
                action: 'login',
                csrfmiddlewaretoken: Cookies.get('csrftoken'),
            },
            success: function (response) {
                $('#main-form').html(response)
            },
            error: function () {
                console.log('internal error.')
            },
        })
        reset_password_handler()
        registration_handler()
    })
}


$(document).keyup(function(e) {
    if (e.keyCode === 13) {
        $('.major-button').click();
    } else if (e.keyCode === 27) {
        $('#change-to-login-form').click()
    }
})


function login_button_handler () {

    $(document).on('click', '#login-button', function () {
        let username = $('#username').val();
        let password = $('#password').val();
        if((username !== "") && (password !== "")){
            $.ajax({
                url: '/',
                type: 'POST',
                data: {
                    action: 'login-to-system',
                    username: username,
                    password: password,
                    csrfmiddlewaretoken: Cookies.get('csrftoken'),
                },
                success: function(response){
                    $('body').html(response)
                },
                error: function(){
                    console.log('internal error.')
                },
            });
        } else {
            console.log("missing username or password.")
        }
    })
}


reset_password_handler()
registration_handler()
login_handler()
login_button_handler()
