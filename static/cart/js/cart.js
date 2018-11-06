$(function () {
    $('.cart').width(innerWidth)
    caltotal()

    //点击勾选或取消
    $('.confirm-wrapper').click(function () {
        var $that = $(this)

        if ($(this).find('.glyphicon-ok').length){
            $(this).find('.glyphicon-ok').removeAttr()
        }
    })

    //计算总价格
    function caltotal() {
        var price_all = 0
        $('.goods').each(function () {
            var $confirm = $(this).find('.confirm-wrapper')
            var $content = $(this).find('.content-wrapper')

            if ($confirm.find('.glyphicon-ok').length) {}
                var num = parseFloat($content.find('.num').attr('attr')) //数量
                var price = parseFloat($content.find('.price').attr('attr')) //价格
                price_all += num * price
        })

        $('.bill .total b').html(price_all)
    }
})