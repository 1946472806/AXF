$(function () {
    $('.cart').width(innerWidth)
    var selall = true
    caltotal()

    //商品选择，或取消选择
    $('.cart .confirm-wrapper').click(function () {
        var cartid = $(this).attr('cartid')
        var $that = $(this)

        selall = true
        //发起ajax请求,将购物车里面的这个商品的选择状态改变一下
        $.get('/axf/changesel/',{'cartid':cartid},function (data) {
            if (data['backstatus'] == 1){
                if ($that.find('.glyphicon-ok').length){
                    $that.find('span').removeClass('glyphicon-ok').addClass('no')
                }else {
                    $that.find('span').removeClass('no').addClass('glyphicon glyphicon-ok')
                }
            }
            //重新计算金额
            caltotal()
        })
    })

    //全选或取消全选
    $('.cart .bill .all').click(function () {
        var $sel = $(this)
        var $shops = $('.cart .confirm-wrapper')

        selall = true
        if ($sel.find('.no').length){ //没有全选的情况下
            //发起ajax请求,将购物车里面的这个用户的全部商品的选择状态改成True
            $.get('/axf/changeall/',{'flag':'1'},function (data) {
                if (data['backstatus'] == 1) {
                    $shops.each(function () {
                        $(this).find('span').removeClass('no').addClass('glyphicon glyphicon-ok')
                    })
                }
                //重新计算金额
                caltotal()
                //本身的图标改一下
                $sel.find('span').removeClass('no').addClass('glyphicon glyphicon-ok')
            })

        }else {
            //发起ajax请求,将购物车里面的这个用户的全部商品的选择状态改成False
            $.get('/axf/changeall/',{'flag':'0'},function (data) {
                if (data['backstatus'] == 1) {
                    $shops.each(function () {
                        $(this).find('span').removeClass('glyphicon glyphicon-ok').addClass('no')
                    })
                }
                //重新计算金额
                caltotal()
                //本身的图标改一下
                $sel.find('span').removeClass('glyphicon glyphicon-ok').addClass('no')
            })
        }
    })

    //计算总价格
    function caltotal() {
        var price_all = 0
        $('.cart .goods').each(function () {
            var $confirm = $(this).find('.confirm-wrapper')
            var $content = $(this).find('.content-wrapper')

            if ($confirm.find('.glyphicon-ok').length) {
                var num = parseFloat($content.find('.num').attr('attr')) //数量
                var price = parseFloat($content.find('.price').attr('attr')) //价格
                price_all += num * price
            }else {
                selall = false
            }
            })

        if (price_all > 0){
            price_all = price_all.toFixed(2) //保留两位小数
        }
        //显示总金额
        $('.cart .bill .total b').html(price_all)
        //全选按钮
        if (selall){
            $('.cart .bill .all').find('span').removeClass('no').addClass('glyphicon glyphicon-ok')
        } else {
            $('.cart .bill .all').find('span').removeClass('glyphicon glyphicon-ok').addClass('no')
        }
    }

    //下单
    $('.cart .bill .bill-right').click(function () {
        var $billright = $(this)
        //发起ajax请求
        $.get('/axf/placeorder/',{'test':'1111'},function (data) {
            if (data['backstatus'] == '1'){
                var ordernum = data['ordernum']
                //跳转到下单详情界面
                window.open('/axf/getorderinfo/?ordernum='+ordernum,target="_self")
            }
        })
    })
})