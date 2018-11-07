$(function () {
    $('.register').width(innerWidth)

    $('#userid input').blur(function () {
        if($(this).val() == '') return
        //发起ajax请求，验证用户是否已经存在
        $.get('/axf/verifyuser/',{'useriderror':$(this).val()},function (data) {
            if (data['backstatus'] == 0){ //已经存在此用户
                $('#userid i').html(data['msg'])
                $('#userid').removeClass('has-success').addClass('has-error')
                $('#userid span').removeClass('glyphicon-ok').addClass('glyphicon-remove')
            } else {
                $('#userid i').html('')
                $('#userid').removeClass('has-error').addClass('has-success')
                $('#userid span').removeClass('glyphicon-remove').addClass('glyphicon-ok')
            }
        })
    })

    //密码格式检验
    $('#password input').blur(function () {
        if($(this).val() == '') return

        var password = $(this).val()
        if (password.length < 6 || password.length > 12 ){
            $('#password i').html('密码长度为6~16个字符')
            $('#password').removeClass('has-success').addClass('has-error')
            $('#password span').removeClass('glyphicon-ok').addClass('glyphicon-remove')
        } else {
            $('#password i').html('')
            $('#password').removeClass('has-error').addClass('has-success')
            $('#password span').removeClass('glyphicon-remove').addClass('glyphicon-ok')
        }
    })

    //检验确认密码
    $('#verifypassword input').blur(function () {
        if($(this).val() == '') return

        var verifypassword = $(this).val()
        if (verifypassword.length < 6 || verifypassword.length > 12 || verifypassword != $('#password input').val()) {
            $('#verifypassword i').html('两次密码不一致')
            $('#verifypassword').removeClass('has-success').addClass('has-error')
            $('#verifypassword span').removeClass('glyphicon-ok').addClass('glyphicon-remove')
        }else {
            $('#verifypassword i').html('')
            $('#verifypassword').removeClass('has-error').addClass('has-success')
            $('#verifypassword span').removeClass('glyphicon-remove').addClass('glyphicon-ok')
        }
    })

    // 名字
    $('#nickname input').blur(function () {
        if($(this).val() == '') return

        $('#nickname').removeClass('has-error').addClass('has-success')
        $('#nickname span').removeClass('glyphicon-remove').addClass('glyphicon-ok')
    })

    //检测手机号码
    var telok = /^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$/;
    $('#telphone input').blur(function () {
        if($(this).val() == '') return

        var check = telok.test($(this).val()) //是否匹配
        if (check){
           $('#telphone i').html('')
            $('#telphone').removeClass('has-error').addClass('has-success')
            $('#telphone span').removeClass('glyphicon-remove').addClass('glyphicon-ok')
        } else {
            $('#telphone i').html('请输入正确的手机号')
            $('#telphone').removeClass('has-success').addClass('has-error')
            $('#telphone span').removeClass('glyphicon-ok').addClass('glyphicon-remove')
        }
    })

    // 地址
    $('#address input').blur(function () {
        if($(this).val() == '') return

        $('#address').removeClass('has-error').addClass('has-success')
        $('#address span').removeClass('glyphicon-remove').addClass('glyphicon-ok')
    })
})