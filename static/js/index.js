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


reset_password_handler()
registration_handler()
login_handler()


$(document).keyup(function(e) {
    if (e.keyCode === 13) {
        $('.major-button').click();
    } else if (e.keyCode === 27) {
        $('#change-to-login-form').click()
    }
})
