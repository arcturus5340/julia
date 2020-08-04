registration =
    "<form class='box' name='login-form'> \
        <h2>Let's get acquainted!</h2> \
        <div class='login-info'>I need your future username,</div> \
        <div class='login-info'>your e-mail & your future password.</div> \
        <input type='text' name='reg-Username' id='reg-username' placeholder='Username'> \
        <input type='text' name='reg-E-mail' id='reg-e-mail' placeholder='E-mail'> \
        <input type='password' name='reg-Password' id='reg-password' placeholder='Password'> \
        <button class='login-button' type='button' name='Login' value='Login'>Sign Up</button> \
        <div class='back-to-login'>\
            <a href='#' id='back-to-login'>We're already acquainted.</a>\
        </div>\
        <a href='https://github.com/arcturus5340/julia' class='social-circle icoGitHub' title='GitHub'><i class='fab fa-github'></i></a>\
    </form>"

function compare_inputs(){
    if (($('#Username').val() == $('#Password').val()) &&
        ($('#Username').val()) && ($('#Username').val())) {
        console.log('true');
    }
}

$('#username').keyup(compare_inputs);

$('#password').keyup(compare_inputs);

$('#registration').click(function () {
    $('#login-form').html(registration)
})
