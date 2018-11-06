$(function () {
    // 滚动条处理
    $('.market').width(innerWidth)


    // 获取下标 typeIndex
    typeIndex = $.cookie('typeIndex')
    if(typeIndex){  // 存在，对应分类
        $('.type-slider .type-item').eq(typeIndex).addClass('active')
    } else {    // 不存在，默认就是热榜
        $('.type-slider .type-item:first').addClass('active')
    }


    // 侧边栏点击处理 (页面会重新加载)
    $('.type-slider .type-item').click(function () {
        // 保存下标
        // console.log($(this).index())
        // 保存下标 cookie
        $.cookie('typeIndex', $(this).index(),{exprires:3, path:'/'})
    })



    // 分类 和 排序
    var alltypeBt = false
    var mysortBt = false
    $('#myallBt').click(function () {
        // 取反
        alltypeBt = !alltypeBt

        if (alltypeBt){ // 显示
            $('.bounce-view.type-view').show()
            $('#myallBt b').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')

            mysortBt = false
            $('.bounce-view.sort-view').hide()
            $('#mysortBt b').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')
        } else {    // 隐藏
            $('.bounce-view.type-view').hide()
            $('#myallBt b').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')
        }
    })

    $('#mysortBt').click(function () {
        // 取反
        mysortBt = !mysortBt

        if (mysortBt){ // 显示
            $('.bounce-view.sort-view').show()
            $('#mysortBt b').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')

            alltypeBt = false
            $('.bounce-view.type-view').hide()
            $('#myallBt b').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')
        } else {    // 隐藏
            $('.bounce-view.sort-view').hide()
            $('#mysortBt b').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')
        }
    })

    $('.bounce-view').click(function () {
        alltypeBt = false
        $('.bounce-view.type-view').hide()
        $('#myallBt b').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')

        mysortBt = false
        $('.bounce-view.sort-view').hide()
        $('.bounce-view.sort-view').hide()
        $('#mysortBt b').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up')
    })

    //显示操作
    $('.bt-wrapper .num').each(function () {
        var num = parseInt($(this).html())
        if (num > 0){
            $(this).show()
            $(this).prev().show()
        } else {
             $(this).hide()
            $(this).prev().hide()
        }
    })

    //加
    $('.bt-wrapper .glyphicon-plus').click(function () {
        var goodsid = $(this).attr('goodsid')
        var $obj = $(this)
        //发起ajax请求
        $.get('/addcarts/',{'goodsid':goodsid},function (data) {
            if (data['backstatus'] == '-1'){
                //重定向到登录页面
                window.open('/login/',target="_self")
            } else {
                $obj.prev().html(data['number']).show()
                $obj.prev().prev().show()
            }
        })
    })

    //减
    $('.bt-wrapper .glyphicon-minus').click(function () {
        var goodsid = $(this).attr('goodsid')
        var $obj = $(this)
        //发起ajax请求
        $.get('/subcarts/',{'goodsid':goodsid},function (data) {
            if (data['backstatus'] == '-1'){
                //重定向到登录页面
                window.open('/login/',target="_self")
            } else {
                if (data['number'] == 0){
                    $obj.next().hide()
                    $obj.hide()
                } else {
                    $obj.next().html(data['number']).show()
                    $obj.show()
                }
            }
        })
    })

})