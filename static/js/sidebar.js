$(function () {
    $('.sidebar-dismiss').on('click', function() {
        $('.sidebar').removeClass('active');
        $('.content').removeClass('sidebar-is-active');
    });

    $('.sidebar-open').on('click', function() {
        $('.sidebar').addClass('active');
        $('.content').addClass('sidebar-is-active');
    });
})
