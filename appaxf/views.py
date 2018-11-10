import hashlib
import os
import random
import time
import uuid

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from AXF import settings
from appaxf.alipay import alipay_axf
from appaxf.models import Wheel, Nav, Mustbuy, Shop, MainShow, Foodtypes, Goods, User, Cart, Order, Orderinfo


# 首页
def home(request):
    #顶部轮播图数据
    wheels = Wheel.objects.all()

    #导航
    navs = Nav.objects.all()

    #每日必购
    mustbuys = Mustbuy.objects.all()

    #部分商品
    shoplist = Shop.objects.all()
    shophead = shoplist[0]
    shoptab = shoplist[1:3]
    shopclass = shoplist[3:7]
    shopcommend = shoplist[7:11]

    #商品主体
    mainshows = MainShow.objects.all()

    data = {
        'wheels':wheels,
        'navs':navs,
        'mustbuys':mustbuys,
        'shophead':shophead,
        'shoptab':shoptab,
        'shopclass':shopclass,
        'shopcommend':shopcommend,
        'mainshows':mainshows,
    }
    return render(request, 'home/home.html',context=data)

# 闪购超市
def market(request, categoryid, childid, sortid):
    #商品分类数据
    foodtypes = Foodtypes.objects.all()

    # 获取点击 历史
    typeIndex = int(request.COOKIES.get('typeIndex', 0))
    categoryid = foodtypes[typeIndex].typeid

    #此大类对应下的子类
    chidnames = foodtypes.get(typeid=categoryid).childtypenames
    chidlist = []
    for chidname in chidnames.split('#'):
        arr = chidname.split(':')
        obj = {'childname':arr[0], 'childid':arr[1]}
        chidlist.append(obj)

    # 根据商品分类 数据过滤
    if childid == '0':  # 全部分类
        goodslist = Goods.objects.filter(categoryid=categoryid)
    else: # 对应分类
        goodslist = Goods.objects.filter(categoryid=categoryid, childcid=childid)

    if sortid == '1': #销量排序
        goodslist = goodslist.order_by('productnum')
    elif sortid == '2': #价格最低
        goodslist = goodslist.order_by('price')
    elif sortid == '3': #价格最高
        goodslist = goodslist.order_by('-price')

    #登录用户购物车信息
    token = request.session.get('username')
    carts = []
    if token:
        user = User.objects.get(token=token)
        carts = Cart.objects.filter(user=user).exclude(number=0)

    data = {
        'foodtypes':foodtypes,
        'goodslist': goodslist,
        'childid': childid,
        'carts':carts,
        'chidlist':chidlist,
        'categoryid': categoryid,
    }

    return render(request, 'market/market.html',context=data)

# 购物车
def cart(request):
    token = request.session.get('username')
    carts = []
    if token:
        user = User.objects.get(token=token)
        carts = Cart.objects.filter(user=user).exclude(number=0)
        return render(request, 'cart/cart.html',{'carts':carts})
    else:
        return redirect('appaxf:login')

# 我的
def mine(request):
    token = request.session.get('username')
    data = {}
    #未登录
    if not token:
        data['user'] = '未登录(点击登录)'
        data['rank'] = '无等级'
        data['img'] = '/static/uploads/axf.png'
        data['flag'] = False
    else:
        user = User.objects.filter(token=token).first()
        # 待付款
        nopaynum = Order.objects.filter(user=user).filter(status=1).count()
        #待收货
        nogetgood = Order.objects.filter(user=user).filter(status=3).count()
        #待评价
        noevaluation = Order.objects.filter(user=user).filter(status=4).count()
        #退款/售后
        refund = Order.objects.filter(user=user).filter(status=6).count()

        data['user'] = user.name
        data['rank'] = user.rank
        data['img'] = '/static/uploads/' + user.img
        data['flag'] = True
        data['nopaynum'] = nopaynum
        data['nogetgood'] = nogetgood
        data['noevaluation'] = noevaluation
        data['refund'] = refund
    #已登录
    return render(request, 'mine/mine.html',context=data)

#注册
def register(request):
    if request.method == 'GET':
        return render(request,'mine/register.html')
    elif request.method == 'POST':
        user = User()
        user.userid = request.POST.get('userid')
        user.password = generate_password(request.POST.get('password'))
        user.name = request.POST.get('nickname')
        user.tel = request.POST.get('telphone')
        user.address = request.POST.get('address')
        #头像
        img_name = user.userid + '.png'
        img_savepath = os.path.join(settings.MEDIA_ROOT,img_name)
        files = request.FILES.get('file')
        with open(img_savepath,'wb') as fp:
            for file in files.chunks():
                fp.write(file)
        user.img =img_name
        #用uuid方式生成
        user.token = str(uuid.uuid5(uuid.uuid4(), 'register'))
        try:
            user.save()
        except Exception as e:
            return HttpResponse('保存数据失败!' + str(e))

        #这里状态先不保持，注册和登录模块区分开
        #页面重定向到我的
        return redirect('appaxf:mine')

# 检测用户
def verifyuser(request):
    userid = request.GET.get('useriderror')
    try:
        user = User.objects.get(userid=userid)
        return JsonResponse({'msg':'用户已经存在!','backstatus':'0'})
    except:
        return JsonResponse({'msg': '用户有效!', 'backstatus': '1'})
#密码加密
def generate_password(password):
    sha = hashlib.sha512()
    sha.update(password.encode('utf-8'))
    return sha.hexdigest()

# 登录
def login(request):
    if request.method == 'GET':
        return render(request,'mine/login.html')
    elif request.method == 'POST':
        userid = request.POST.get('userid')
        password = generate_password(request.POST.get('password'))

        #检测账号和密码是否正确
        users = User.objects.filter(userid=userid,password=password)
        if not users.count():
            msg = '账号密码错误!'
            return render(request,'mine/login.html',{'msg':msg})

        #更新并保存当前状态
        user = users.first()
        user.token = str(uuid.uuid5(uuid.uuid4(), 'login'))
        user.save()
        request.session['username'] = user.token
        return redirect('appaxf:mine')
# 注销
def loginout(request):
    request.session.flush()
    return redirect('appaxf:mine')

#加
def addcarts(request):
    goodsid = request.GET.get('goodsid')
    token = request.session.get('username')

    if token: #已登录
        try:
           user = User.objects.get(token=token)
           goods = Goods.objects.get(pk=goodsid)

           carts = Cart.objects.filter(user=user,goods=goods)
           if carts.count():
               cart = carts.first()
               cart.number += 1
               cart.save()
               return JsonResponse({'msg': '添加数量成功!', 'number':cart.number,'backstatus': '1'})
           else:
               cart = Cart()
               cart.user = user
               cart.goods = goods
               cart.number = 1
               cart.save()
               return JsonResponse({'msg': '添加数量成功!','number':1, 'backstatus': '1'})
        except Exception as e:
            return JsonResponse({'msg': '数据有误!', 'backstatus': '-1'})
    else: #未登录
        return JsonResponse({'msg': '还没有登录!', 'backstatus': '-1'})

#减
def subcarts(request):
    goodsid = request.GET.get('goodsid')
    token = request.session.get('username')

    #不用再判断是否登录,能到这个路由函数说明已经登录了
    try:
        user = User.objects.get(token=token)
        goods = Goods.objects.get(pk=goodsid)

        carts = Cart.objects.filter(user=user, goods=goods)
        cart = carts.first()
        cart.number -= 1
        cart.save()
        return JsonResponse({'msg': '减少数量成功!', 'number': cart.number, 'backstatus': '1'})

    except Exception as e:
        return JsonResponse({'msg': '数据有误!', 'backstatus': '-1'})

#选择或取消选择
def changesel(request):
    cartid = request.GET.get('cartid')

    try:
        cart = Cart.objects.filter(pk=cartid).first()
        cart.isselect = not cart.isselect
        cart.save()
        return JsonResponse({'msg':'数据状态改变成功!','backstatus':'1'})
    except Exception as e:
        return JsonResponse({'msg': '数据状态改变失败!', 'backstatus': '-1'})

# 全选或全消
def changeall(request):
    flag = request.GET.get('flag')
    token = request.session.get('username')
    if flag == '1':  # 全选
        isselect = 1
    else:  # 全消
        isselect = 0
    try:
        user = User.objects.get(token=token)
        carts = Cart.objects.filter(user=user)
        for cart in carts:
            cart.isselect = isselect
            cart.save()
        return JsonResponse({'msg':'反选成功!','backstatus':'1'})

    except Exception as e:
        return JsonResponse({'msg': '保存数据失败!', 'backstatus': '-1'})

#下单
def placeorder(request):
    token = request.session.get('username')
    user = User.objects.get(token=token)

    try:
        carts = Cart.objects.filter(user=user,isselect=1)
        #订单号
        ordernum = str(uuid.uuid5(uuid.uuid4(), 'order'))
        order = Order.createorder(user, ordernum)
        order.save()
        #生成订单主表和明细表数据
        for cart in carts:
            orderinfo = Orderinfo.createorderinfo(order,cart.goods,cart.number)
            orderinfo.save()
            # 删除相应购物车数据
            cart.delete()
        #跳转到已下单界面
        return JsonResponse({'msg':'下单成功！','ordernum':ordernum,'backstatus': '1'})
    except Exception as e:
        return JsonResponse({'msg': '下单失败!', 'backstatus': '-1'})

#下单详情
def getorderinfo(request):
    ordernum = request.GET.get('ordernum')

    order = Order.objects.get(ordernum=ordernum)
    return render(request,'order/orderinfo.html',{'order':order})

# 支付完成后，支付宝调用的(通知AXF服务端)
def notifyurl(request):
    if request.method == "POST":
        # 检测是否支付成功
        # 去请求体中获取所有返回的数据：状态/订单号
        from urllib.parse import parse_qs
        # name&age=123....
        body_str = request.body.decode('utf-8')
        post_data = parse_qs(body_str)

        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]

        # post_dict有10key： 9 ，1
        sign = post_dict.pop('sign', None)
        status = alipay_axf.verify(post_dict, sign) #POST验证 True

        #返回接收到的数据post_dict如下：
        # {'gmt_create': '2018-11-09 21:47:10', 'charset': 'utf-8', 'gmt_payment': '2018-11-09 21:47:26',
        #  'notify_time': '2018-11-09 21:47:27', 'subject': '测试订单 --- iphone XX', 'buyer_id': '2088102176438721',
        #  'invoice_amount': '1.10', 'version': '1.0', 'notify_id': '9196624f14c7d2f4a91eaff2a9c4042lk5',
        #  'fund_bill_list': '[{"amount":"1.10","fundChannel":"ALIPAYACCOUNT"}]', 'notify_type': 'trade_status_sync',
        #  'out_trade_no': '15', 'total_amount': '1.10', 'trade_status': 'TRADE_SUCCESS',
        #  'trade_no': '2018110922001438720500754426', 'auth_app_id': '2016091900547441', 'receipt_amount': '1.10',
        #  'point_amount': '0.00', 'app_id': '2016091900547441', 'buyer_pay_amount': '1.10',
        #  'seller_id': '2088102176328329'}

        #得到订单号
        out_trade_no = post_dict['out_trade_no']

        # 这里应该根据返回的状态和单据号更新用户订单表中的订单状态
        Order.objects.filter(pk=out_trade_no).update(status=2)
        return JsonResponse({'msg': 'success'})

# 支付完成后，AXF客户端跳转的页面
def returnurl(request):
    #这里暂时跳转到‘我的’页面
    return redirect('appaxf:mine')

#支付宝支付
def pay(request):
    orderid = request.GET.get('orderid')
    # 支付url
    url = alipay_axf.direct_pay(
        subject='测试订单 --- iphone XX',  # 订单名称
        out_trade_no=orderid,  # 订单号
        total_amount=1.1,  # 付款金额
        # return_url='http://112.74.55.3/axf/returnurl/'
        return_url='http://120.78.160.121/axf/returnurl/'
    )

    # 拼接支付网关
    # alipay_url = 'https://openapi.alipaydev.com/gateway.do?{data}'.format(data=url)
    alipay_url = 'https://openapi.alipaydev.com/gateway.do?{data}'.format(data=url)

    return JsonResponse({'alipay_url': alipay_url})

#我的全部订单
def getallorderinfo(request):
    token = request.session.get('username')
    data = {}
    if token:
        user = User.objects.get(token=token)

        # 订单状态(1.未付款 2.已付款未发货 3.已发货未收货 4.已收货未评价 5.已评价 6.退款)
        # 未付款
        nopaynums = Order.objects.filter(user=user).filter(status=1)
        #已付款未发货
        nodeliverys = Order.objects.filter(user=user).filter(status=2)
        # 已发货未收货
        nogetgoods = Order.objects.filter(user=user).filter(status=3)
        # 已收货未评价
        noevaluations = Order.objects.filter(user=user).filter(status=4)
        #已评价
        evaluations = Order.objects.filter(user=user).filter(status=5)
        # 退款/售后
        refunds = Order.objects.filter(user=user).filter(status=6)

        data['nopaynums'] = nopaynums
        data['nodeliverys'] = nodeliverys
        data['nogetgoods'] = nogetgoods
        data['noevaluations'] = noevaluations
        data['evaluations'] = evaluations
        data['refunds'] = refunds
        return render(request, 'order/allorderinfo.html', context=data)
    else:
        return redirect('appaxf:login')