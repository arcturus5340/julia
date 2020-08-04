login =
    "<h2>Hi, I'm Julia.</h2>\n" +
    "<div class=\"login-info\">Tell me your username and password.</div>\n" +
    "<input type=\"text\" name=\"Username\" id=\"username\" placeholder=\"Username\">\n" +
    "<input type=\"password\" name=\"Password\" id=\"password\" placeholder=\"Password\" autocomplete=\"on\">\n" +
    "<button class=\"major-button\" type=\"button\" name=\"Login\" value=\"Login\" href=\"#\">Login</button>\n" +
    "<div class=\"unusual-actions\">\n" +
    "    <div class=\"reset-password\"><span id=\"reset-password\">I forgot my password.</a></div>\n" +
    "    <div class=\"unusual-actions-sep\">||</div>\n" +
    "    <div class=\"registration\"><span id=\"registration\">We're not acquainted.</a></div>\n" +
    "</div>\n" +
    "<a href=\"https://github.com/arcturus5340/julia\" class=\"social-circle icoGitHub\" title=\"GitHub\"><i class=\"fab fa-github\"></i></a>\n"

reset_password =
    "<h2>Oh, let me help you.</h2>\n" +
    "<div class=\"login-info\">Tell me your username or e-mail.</div>\n" +
    "<div class=\"login-info\">I'll send you a link to get back into your account.</div>\n" +
    "<input type=\"text\" name=\"UsernameOrEmail\" id=\"UsernameOrEmail\" placeholder=\"Username or e-mail\">\n" +
    "<button class=\"major-button\" type=\"button\" name=\"Send\" value=\"Send\" href=\"#\">Send</button>\n" +
    "<div class=\"back-to-login\">\n" +
    "    <span id=\"login\">I remembered my password.</a>\n" +
    "</div>\n" +
    "<a href=\"https://github.com/arcturus5340/julia\" class=\"social-circle icoGitHub\" title=\"GitHub\"><i class=\"fab fa-github\"></i></a>\n"

registration =
    "<h2>Let's get acquainted!</h2> \n" +
    "<div class=\"login-info\">I need your future username,</div> \n" +
    "<div class=\"login-info\">your e-mail & your future password.</div> \n" +
    "<input type=\"text\" name=\"reg-Username\" id=\"reg-username\" placeholder=\"Username\"> \n" +
    "<input type=\"text\" name=\"reg-E-mail\" id=\"reg-e-mail\" placeholder=\"E-mail\"> \n" +
    "<input type=\"password\" name=\"reg-Password\" id=\"reg-password\" placeholder=\"Password\" autocomplete=\"on\"> \n" +
    "<button class=\"major-button\" type=\"button\" name=\"Login\" value=\"Login\">Sign Up</button> \n" +
    "<div class=\"back-to-login\">\n" +
    "    <span id=\"login\">We're already acquainted.</a>\n" +
    "</div>\n" +
    "<a href=\"https://github.com/arcturus5340/julia\" class=\"social-circle icoGitHub\" title=\"GitHub\"><i class=\"fab fa-github\"></i></a>"

$('#registration').on('click', function () {
    console.log("Changed to registration form.");
    $('#main-form').html(registration);
})

$('#reset-password').on('click', function () {
    console.log("Changed to reset password form.");
    $('#main-form').html(reset_password);
})

$(document).on('click', '#login',function () {
    console.log("Changed to login form.");
    $('#main-form').html(login);
    $(document).on('click', '#reset-password',function () {
        console.log("Changed to login form.");
        $('#main-form').html(reset_password);
    })
})

$(document).on('click', '#login',function () {
    console.log("Changed to login form.");
    $('#main-form').html(login);
    $(document).on('click', '#registration',function () {
        console.log("Changed to login form.");
        $('#main-form').html(registration);
    })
})

$(document).keyup(function(e) {
    if (e.keyCode === 13) {
        $('.major-button').click();
    }
    if (e.keyCode === 27) {
        $('#main-form').html(login);$(document).on('click', '#reset-password',function () {
            console.log("Changed to login form.");
            $('#main-form').html(reset_password);
        });
        $(document).on('click', '#registration',function () {
            console.log("Changed to login form.");
            $('#main-form').html(registration);
        })
    };
})

$('.major-button').on('click',function () {
    console.log("Major button has been clicked.");
})
