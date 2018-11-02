from django.http import HttpResponse
from django.shortcuts import render
from appaxf.models import Wheel, Nav, Mustbuy, Shop, MainShow, Foodtypes, Goods, User, Cart


def home(request):  # 首页
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


def market(request, categoryid, childid, sortid):    # 闪购超市
    #商品分类数据
    foodtypes = Foodtypes.objects.all()

    # 获取点击 历史 [typeIndex]
    # 有typeIndex
    # 无typeIndex，默认0
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
    token = request.session.get('token')
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


def cart(request):  # 购物车
    return render(request, 'cart/cart.html')


def mine(request):  # 我的
    return render(request, 'mine/mine.html')