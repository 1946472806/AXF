import hashlib
import os
import uuid

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from AXF import settings
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


def cart(request):  # 购物车
    token = request.session.get('username')
    carts = []
    if token:
        user = User.objects.get(token=token)
        carts = Cart.objects.filter(user=user).exclude(number=0)
        return render(request, 'cart/cart.html',{'carts':carts})
    else:
        return redirect('appaxf:login')


def mine(request):  # 我的
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
        data['user'] = user.name
        data['rank'] = user.rank
        data['img'] = '/static/uploads/' + user.img
        data['flag'] = True
    #已登录
    return render(request, 'mine/mine.html',context=data)


def register(request): #注册
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


def verifyuser(request): # 检测用户
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

