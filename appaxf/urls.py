from django.conf.urls import url

from appaxf import views

urlpatterns = [
    url(r'^$', views.home, name='index'),  # 首页
    url(r'^home/$', views.home, name='home'),   # 首页
    url(r'^market/(\d+)/(\d+)/(\d+)/$', views.market, name='market'), # 闪购超市
    url(r'^cart/$', views.cart, name='cart'),   # 购物车
    url(r'^mine/$', views.mine, name='mine'),   # 我的
    url(r'^register/$', views.register, name='register'),   # 注册
    url(r'^verifyuser/$', views.verifyuser, name='verifyuser'),   # 检测用户
    url(r'^login/$', views.login, name='login'),   # 登录
    url(r'^loginout/$', views.loginout, name='loginout'),   # 退出登录
    url(r'^addcarts/$', views.addcarts, name='addcarts'),   # 添加购物车
    url(r'^subcarts/$', views.subcarts, name='subcarts'),  # 减少购物车
    url(r'^changesel/$', views.changesel, name='changesel'),  # 选择或取消选择
    url(r'^changeall/$', views.changeall, name='changeall'),  # 全选或全消
    url(r'^placeorder/$', views.placeorder, name='placeorder'), #下单
    url(r'^getorderinfo/$', views.getorderinfo, name='getorderinfo'), #下单详情
]