from django.shortcuts import render
from appaxf.models import Wheel, Nav, Mustbuy


def home(request):  # 首页
    #顶部轮播图数据
    wheels = Wheel.objects.all()
    #导航
    navs = Nav.objects.all()
    #每日必购
    mustbuys = Mustbuy.objects.all()

    data = {
        'wheels':wheels,
        'navs':navs,
        'mustbuys':mustbuys,
    }
    return render(request, 'home/home.html',context=data)


def market(request):    # 闪购超市
    return render(request, 'market/market.html')


def cart(request):  # 购物车
    return render(request, 'cart/cart.html')


def mine(request):  # 我的
    return render(request, 'mine/mine.html')