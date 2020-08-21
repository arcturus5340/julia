$(document).on('animationend webkitAnimationEnd onAnimationEnd', '#form-info', function () {
    $('#form-info').removeClass('shake');
})


$(".upload-solution").on("change", function() {
    let file_name = $(this).val().split("\\").pop();
    if (file_name !== '')
        $(this).siblings(".upload-solution-label").addClass("selected").html(file_name)
    else
        $(this).siblings(".upload-solution-label").addClass("selected").html("You haven't choose a file, try again!")

});


$('.sidebar-dismiss').on('click', function() {
    $('.sidebar').removeClass('active');
    $('.content').removeClass('sidebar-is-active');
});

$('.sidebar-open').on('click', function() {
    $('.sidebar').addClass('active');
    $('.content').addClass('sidebar-is-active');
});


function change_to_reset_form () {

    $(document).on('click', '#change-to-reset-password-form', function () {
        $.ajax({
            url: '/login/change-to-reset-form/',
            type: 'POST',
            data: {
                action: 'reset-password',
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
            url: '/login/change-to-registration-form/',
            type: 'POST',
            data: {
                action: 'registration',
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
            url: '/login/change-to-login-form/',
            type: 'POST',
            data: {
                action: 'login',
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


$(document).keyup(function(e) {
    if (e.keyCode === 13)
        $('.major-button').click()
    else if (e.keyCode === 27)
        $('#change-to-login-form').click()
    else if (e.keyCode === 37)
        $('.sidebar-dismiss').click()
    else if (e.keyCode === 39)
        $('.sidebar-open').click()
})


function login_handler () {
    $(document).on('click', '#login-button', function () {
        let username = $('#username').val();
        let password = $('#password').val();
        let form_info = $('#form-info');
        if((username !== "") && (password !== "")){
            $.ajax({
                url: 'login/',
                type: 'POST',
                data: {
                    username: username,
                    password: password,
                    csrfmiddlewaretoken: Cookies.get('csrftoken'),
                },
                success: function(response){
                    if (response['status'] === 'ok') {
                        $('body').html(response['content'])
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
                url: 'registration/',
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
                url: 'reset-password/',
                type: 'POST',
                data: {
                    user_key: user_key,
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
        } else {
            form_info.html('Sorry, I can read neither neither your username nor e-mail.');
            form_info.addClass('shake');
        }
    })
}

$('a.nav-link').on('show.bs.tab', function (e) {
    let tab_content = $('.tab-content')
    if ( $(e.target.getAttribute('href')).height() > $(window).height() ) {
        setTimeout(function () {
            tab_content.addClass('large')
        }, 150)
    } else {
        setTimeout(function () {
            tab_content.removeClass('large')
        }, 150)    }
})

change_to_reset_form()
change_to_registration_form()
change_to_login_form()
login_handler()
registration_handler()
reset_password_handler()