$(function () {
    $('.orderinfo').width(innerWidth)

    //付款
    $('#pay').click(function () {
        var orderid = $(this).attr('orderid')
        console.log('支付' + orderid)

        $.get('/axf/pay/',{'orderid':orderid},function (data) {
            console.log(data['alipay_url'])
            window.open(data['alipay_url'], target='_self')
        })

    })
})