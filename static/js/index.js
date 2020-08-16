$(document).on('animationend webkitAnimationEnd onAnimationEnd', '#form-info', function () {
    $('#form-info').removeClass('shake');
})

function change_to_reset_form () {

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


function change_to_registration_form () {

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


function change_to_login_form () {

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
        change_to_reset_form()
        change_to_registration_form()
    })
}


$(document).keyup(function(e) {
    if (e.keyCode === 13) {
        $('.major-button').click();
    } else if (e.keyCode === 27) {
        $('#change-to-login-form').click()
    }
})


function login_handler () {
    $(document).on('click', '#login-button', function () {
        let username = $('#username').val();
        let password = $('#password').val();
        let form_info = $('#form-info');
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
            let forgotten_form = [];
            if (username === '')
                forgotten_form.push('username');
            if (password === '')
                forgotten_form.push('password');
            form_info.html('Sorry, you forgot to enter your ' + forgotten_form.join(' & ') + '.');
            form_info.addClass('shake');
        }
    })
}


function registration_handler () {
    $(document).on('click', '#sign-up-button', function () {
        let username = $('#reg-username').val();
        let email = $('#reg-e-mail').val();
        let password = $('#reg-password').val();
        let form_info = $('#form-info');
        if((username !== "") && (password !== "") && (email !== "")){
            $.ajax({
                url: '/',
                type: 'POST',
                data: {
                    action: 'sign-up-in-system',
                    username: username,
                    email: email,
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
            let forgotten_form = [];
            if (username === '')
                forgotten_form.push('username');
            if (email === '')
                forgotten_form.push('e-mail')
            if (password === '')
                forgotten_form.push('password');
            let answer;
            if (forgotten_form.length === 3)
                answer = forgotten_form.shift() + ', <br>' + forgotten_form.join(' & ')
            else
                answer = forgotten_form.join(' & ')
            console.log(forgotten_form.length);
            form_info.html('Sorry, you forgot to enter your ' + answer + '.');
            form_info.addClass('shake');
        }
    })
}


change_to_reset_form()
change_to_registration_form()
change_to_login_form()
login_handler()
registration_handler()
