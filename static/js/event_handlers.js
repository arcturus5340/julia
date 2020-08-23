$(document).keyup(function(e) {
    if (e.keyCode === 13)
        $('.major-button').click()
    else if (e.keyCode === 27)
        $('#change-to-login-form').click()
    else if (e.keyCode === 37)
        $('.sidebar-dismiss').click()
    else if (e.keyCode === 39)
        $('.sidebar-open').click()
    $(document).on('animationend webkitAnimationEnd onAnimationEnd', '#form-info', function () {
        $('#form-info').removeClass('shake');
    })
})
