$(function () {
    const error_responses = [
        "Great! We did it!",
        "Oh, dear, that's the wrong password. Maybe <br> we aren't just acquainted?",
        "Sorry, but this username is already used.",
        "Excuse me, your e-mail is already in use. Try an <br> another e-mail or reset your password.",
        "You should be very lucky, I guess. Try again please.",
        "Wait, I couldn't send you the verify message. <br> Could you try again please?",
        "Unfortunately, we aren't acquainted yet. Sign up please."
    ]


    function change_to_reset_form () {

        $(document).on('click', '#change-to-reset-password-form', function () {
            $.ajax({
                url: '/auth/get-reset-password-form/',
                type: 'POST',
                data: {
                    csrfmiddlewaretoken: Cookies.get('csrftoken'),
                },
                success: function(response){
                    if (response['status'] === 'ok') {
                        $('#main-form').html(response['content']);
                    }
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
                url: '/auth/get-registration-form/',
                type: 'POST',
                data: {
                    csrfmiddlewaretoken: Cookies.get('csrftoken'),
                },
                success: function(response){
                    if (response['status'] === 'ok') {
                        $('#main-form').html(response['content']);
                    }
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
                url: '/auth/get-login-form/',
                type: 'POST',
                data: {
                    csrfmiddlewaretoken: Cookies.get('csrftoken'),
                },
                success: function (response) {
                    if (response['status'] === 'ok') {
                        $('#main-form').html(response['content']);
                    }
                },
                error: function () {
                    console.log('internal error.')
                },
            })
            change_to_reset_form()
            change_to_registration_form()
        })
    }


    function login_handler () {
        $(document).on('click', '#login-button', function () {
            let username = $('#username').val();
            let password = $('#password').val();
            let form_info = $('#form-info');
            if((username !== "") && (password !== "")){
                $.ajax({
                    url: 'auth/login/',
                    type: 'POST',
                    data: {
                        username: username,
                        password: password,
                        csrfmiddlewaretoken: Cookies.get('csrftoken'),
                    },
                    success: function(response){
                        if (response['status'] === 'ok') {
                            $('body').html(response['content'])
                        } else {
                            form_info.html(error_responses[response['code']]);
                            form_info.addClass('shake');
                        }
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
                    url: 'auth/registration/',
                    type: 'POST',
                    data: {
                        username: username,
                        email: email,
                        password: password,
                        csrfmiddlewaretoken: Cookies.get('csrftoken'),
                    },
                    success: function(response){
                        if (response['status'] === 'ok') {
                            $('#main-form').html(response['content']);
                        } else {
                            form_info.html(error_responses[response['code']]);
                            form_info.addClass('shake');
                        }
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
                form_info.html('Sorry, you forgot to enter your ' + answer + '.');
                form_info.addClass('shake');
            }
        })
    }


    function reset_password_handler () {
        $(document).on('click', '#reset-password-button', function () {
            let user_key = $('#user-key').val();
            let form_info = $('#form-info');
            if(user_key !== ""){
                $.ajax({
                    url: 'auth/reset-password/',
                    type: 'POST',
                    data: {
                        user_key: user_key,
                        csrfmiddlewaretoken: Cookies.get('csrftoken'),
                    },
                    success: function(response){
                        if (response['status'] === 'ok') {
                            $('#main-form').html(response['content']);
                        } else {
                            form_info.html(error_responses[response['code']]);
                            form_info.addClass('shake');
                        }
                    },
                    error: function(){
                        console.log('internal error.')
                    },
                });
            } else {
                form_info.html('Sorry, I can read neither your username nor e-mail.');
                form_info.addClass('shake');
            }
        })
    }


    change_to_reset_form()
    change_to_registration_form()
    change_to_login_form()
    login_handler()
    registration_handler()
    reset_password_handler()
})
