"""final URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import mainsite.views as mainsite

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mainsite.login),
    path('login/', mainsite.login),#mainsite/login/
    path('logout/', mainsite.logout),#mainsite/logout/
    path('register/', mainsite.register),#mainsite/register/
    path('admins/', mainsite.admins),#shopping/admin/
    path('admins/product/delete/<int:del_id>/', mainsite.deleteprod,name='del-prod-url'),#shopping/admin/delete/<int:del_id>/
    path('admins/showproduct/', mainsite.showproduct),#shopping/product/
    path('admins/member/delete/s<int:del_id>/', mainsite.delmember,name='del-user-url'),#shopping/admin/delete_user/<int:del_id>/
    path('admins/showmember/', mainsite.showmember),#shopping/amember/
    path('admins/order/delete/<int:del_id>/', mainsite.delorder,name='del-order-url'),
    path('admins/showorder/', mainsite.showorder),
    path('member/', mainsite.memberproduct,name='user-prod-url' ),#shopping/member/
    path('member/cart/', mainsite.membercart,name='user-cart-url' ),#shopping/cart/
    path('member/cart/remove/<int:rev_id>/', mainsite.removecart,name='user-cart-remove-url' ),#shopping/remove/<int:rev_id>/
    path('member/cart/update/<int:upd_id>/', mainsite.updatecart,name='user-cart-update-url' ),#shopping/update/<int:upd_id>
    path('member/cart/delete/', mainsite.deletecart),#shopping/delete/
    path('member/cart/checkout/', mainsite.checkout),#shopping/checkout/
    
    # path('shopping/admin/update/<int:upd_id>/', mainsite.updonject,name='upd-url'),
]
