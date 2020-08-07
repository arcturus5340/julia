login =
    "<div class=\"login-form\">\n" +
    "    <h2>Hi, I'm Julia.</h2>\n" +
    "    <div class=\"login-info\">Tell me your username and password.</div>\n" +
    "    <label for=\"username\"></label>\n" +
    "    <input type=\"text\" name=\"Username\" id=\"username\" placeholder=\"Username\">\n" +
    "    <label for=\"password\"></label>\n" +
    "    <input type=\"password\" name=\"Password\" id=\"password\" placeholder=\"Password\" autocomplete=\"on\">\n" +
    "    <button class=\"major-button\" type=\"button\" name=\"Login\" value=\"Login\">Login</button>\n" +
    "    <div class=\"unusual-actions\">\n" +
    "        <div class=\"reset-password\"><span id=\"reset-password\">I forgot my password.</span></div>\n" +
    "        <div class=\"unusual-actions-sep\">||</div>\n" +
    "        <div class=\"registration\"><span id=\"registration\">We're not acquainted.</span></div>\n" +
    "    </div>\n" +
    "    <a href=\"https://github.com/arcturus5340/julia\" class=\"social-circle icoGitHub\" title=\"GitHub\"><i class=\"fab fa-github\"></i></a>\n" +
    "</div>"

reset_password =
    "<div class='reset-form'>" +
    "    <h2>Oh, let me help you.</h2>\n" +
    "    <div class=\"login-info\">Tell me your username or e-mail.</div>\n" +
    "    <div class=\"login-info\">I'll send you a link to get back into your account.</div>\n" +
    "    <input type=\"text\" name=\"UsernameOrEmail\" id=\"UsernameOrEmail\" placeholder=\"Username or e-mail\">\n" +
    "    <button class=\"major-button\" type=\"button\" name=\"Send\" value=\"Send\" >Send</button>\n" +
    "    <div class=\"back-to-login\">\n" +
    "        <span id=\"login\">I remembered my password.</a>\n" +
    "    </div>\n" +
    "    <a href=\"https://github.com/arcturus5340/julia\" class=\"social-circle icoGitHub\" title=\"GitHub\"><i class=\"fab fa-github\"></i></a>\n" +
    "</div>"

registration =
    "<div class='registration-form'>" +
    "    <h2>Let's get acquainted!</h2> \n" +
    "    <div class=\"login-info\">I need your future username,</div> \n" +
    "    <div class=\"login-info\">your e-mail & your future password.</div> \n" +
    "    <input type=\"text\" name=\"reg-Username\" id=\"reg-username\" placeholder=\"Username\"> \n" +
    "    <input type=\"text\" name=\"reg-E-mail\" id=\"reg-e-mail\" placeholder=\"E-mail\"> \n" +
    "    <input type=\"password\" name=\"reg-Password\" id=\"reg-password\" placeholder=\"Password\" autocomplete=\"on\"> \n" +
    "    <button class=\"major-button\" type=\"button\" name=\"Login\" value=\"Login\">Sign Up</button> \n" +
    "    <div class=\"back-to-login\">\n" +
    "        <span id=\"login\">We're already acquainted.</a>\n" +
    "    </div>\n" +
    "    <a href=\"https://github.com/arcturus5340/julia\" class=\"social-circle icoGitHub\" title=\"GitHub\"><i class=\"fab fa-github\"></i></a>" +
    "</div>"


function reset_password_handler () {
    main_form = $('#main-form')
    $(document).on('click', '#reset-password', function () {
        main_form.html(reset_password);
    })
}

function registration_handler () {
    main_form = $('#main-form')
    $(document).on('click', '#registration', function () {
        main_form.html(registration);
    })
}


function login_handler () {
    $(document).on('click', '#login', function () {
        main_form = $('#main-form')
        main_form.html(login);
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
        $('#login').click()
    }
})


$('#reset-password').on('click', function () {
    $.ajax({
        url: '',
        type: 'POST',
        data: {
            action: 'reset',
            // csrfmiddlewaretoken: csrfmiddlewaretoken, он здесь же не нужен...
        },
        success: function(response){
            console.log(response)
        },
        error: function(){
            console.log('internal error.')
        },
    });
    // Твое задание:
    // Элемент с id main_form заменить на HTML-код в переменной reset_password
})

$('#registration').on('click', function () {
    $.ajax({
        url: '',
        type: 'POST',
        data: {
            action: 'registration',
            // csrfmiddlewaretoken: csrfmiddlewaretoken, и здесь тоже не нужен...
        },
        success: function(response){
            console.log(response)
        },
        error: function(){
            console.log('internal error.')
        },
    });
    // Твое задание:
    // Элемент с id main_form заменить на HTML-код в переменной registration
})
