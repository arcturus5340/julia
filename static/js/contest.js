$(function () {
    const tab_content = $('.tab-content');

    $.ajax({
        'url': '/api/v1/contests/',
        'type': 'GET',
        'data': {
            csrfmiddlewaretoken: Cookies.get('csrftoken'),
        },
        success: function (response) {
            console.log(response[0])
            for([_, task_url] of response[0]['tasks'].entries()){
                $.ajax({
                    'url': task_url,
                    'type': 'GET',
                    'data': {
                        csrfmiddlewaretoken: Cookies.get('csrftoken'),
                    },
                    success: function (response) {
                        let id = response['id']
                        let title = response['title']
                        console.log(response)
                        $('#contest-tabs').append(task_tab)
                        $('#contest-content').append(task_content)
                    }
                })
            }
        },
    })

    if ( tab_content.height() > Math.ceil($(window).height() * .8) ) {
        tab_content.addClass('large')
    }


    $(window).on('resize', function(){
        if ( tab_content.height() > Math.ceil($(window).height() * .8) ) {
            setTimeout(function () {
                tab_content.addClass('large')
            }, 150)
        } else {
            setTimeout(function () {
                tab_content.removeClass('large')
            }, 150)
        }
    })


    $('a.nav-link').on('show.bs.tab', function (e) {
        if ( $(e.target.getAttribute('href')).height() > Math.ceil($(window).height() * .8) ) {
            setTimeout(function () {
                tab_content.addClass('large')
            }, 150)
        } else {
            setTimeout(function () {
                tab_content.removeClass('large')
            }, 150)
        }
    })


    $(".upload-solution").on("change", function() {
        let file_name = $(this).val().split("\\").pop();
        if (file_name !== '')
            $(this).siblings(".upload-solution-label").addClass("selected").html(file_name)
        else
            $(this).siblings(".upload-solution-label").addClass("selected").html("You haven't choose a file, try again!")

    })
})