from django.urls import path,include
from User import views
app_name="webuser"

urlpatterns = [
    path('homepage/',views.homepage,name="homepage"),
    path('profile/',views.profile,name="profile"),
    path("editprofile/",views.editprofile,name="editprofile"),
    path("changepassword/",views.changepassword,name="changepassword"),
    path('searchshop/',views.searchshop,name="searchshop"),
    path('viewproduct/<str:shid>',views.viewproduct,name="viewproduct"),
    path('ajaxshop/',views.ajaxshop,name="ajaxshop"),
    path('ajaxproduct/',views.ajaxproduct,name="ajaxproduct"),
    path('addtocart/<str:pid>',views.addtocart,name="addtocart"),
    path('mycart/',views.mycart,name="mycart"),
    path('deletecartitem/<str:cid>',views.deletecartitem,name="deletecartitem"),
    path('ajaxmycart/',views.ajaxmycart,name="ajaxmycart"),
    path('payment/',views.payment,name="payment"),
    path('loader/',views.loader,name="loader"),
    path('paymentsuc/',views.paymentsuc,name="paymentsuc"),
    path('mybooking/',views.mybooking,name="mybooking"),
    path('bookedproducts/<str:id>',views.bookedproducts,name="bookedproducts"),
    path('bills/<str:id>',views.bills,name="bills"),
    path('ordercancel/<str:id>',views.ordercancel,name="ordercancel"),
]