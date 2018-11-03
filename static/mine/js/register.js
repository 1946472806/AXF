$(function () {
    $('.register').width(innerWidth)
    $('.tel .glyphicon').hide() //默认不显示手机勾选

    $('#userid').blur(function () {
        //发起ajax请求，验证用户是否已经存在
        $.get('/verifyuser/',{'useriderror':$(this).val()},function (data) {
            if (data['backstatus'] == 0){ //已经存在此用户
                $('#useriderror').show().html(data['msg'])
            } else {
                $('#useriderror').hide()
            }
        })
    })

    //密码格式检验
    $('#password').blur(function () {
        var password = $(this).val()
        if (password.length < 6 || password.length > 12 ){
            $('#passworderror').show()
        } else {
            $('#passworderror').hide()
        }
    })

    //检验确认密码
    $('#verifypassword').blur(function () {
        var verifypassword = $(this).val()
        if (verifypassword.length < 6 || verifypassword.length > 12 || verifypassword != $('#password').val()) {
            $('#verifypassworderror').show()
        }else {
            $('#verifypassworderror').hide()
        }
    })

    //检测手机号码
    var telok = /^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$/;
    $('#telphone').blur(function () {
        var check = telok.test($(this).val()) //是否匹配
        if (check){
            $('.tel').removeClass('has-error').addClass('has-success')
            $('.tel .glyphicon').show().removeClass('glyphicon-remove').addClass('glyphicon-ok')
            $('#subButton').removeAttr('disabled')
        } else {
            $('.tel').removeClass('has-success').addClass('has-error')
            $('.tel .glyphicon').show().removeClass('glyphicon-ok').addClass('glyphicon-remove')
            $('#subButton').attr('disabled','disabled')
        }
    })
})