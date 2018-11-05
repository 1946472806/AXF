$(function () {
    $('.login').width(innerWidth)

    $('#subButton').click(function () {
        if($('#userid input').val() == '' || $('#password input').val() == '') {
            $('#msg').html('账号、密码不能为空!')
            return
        }

    })
})