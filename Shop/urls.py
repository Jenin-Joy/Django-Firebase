from django.urls import path,include
from Shop import views
app_name="webshop"

urlpatterns = [
    path('home/',views.home,name="home"),
    path('profile/',views.profile,name="profile"),
    path('editprofile/',views.editprofile,name="editprofile"),
    path('changepassword/',views.changepassword,name="changepassword"),
    path('addproduct/',views.addproduct,name="addproduct"),
    path('ajaxsubcategory/',views.ajaxsubcategory,name="ajaxsubcategory"),
    path('deleteproduct/<str:did>',views.deleteproduct,name="deleteproduct"),
    path('updatestock/<str:pid>',views.updatestock,name="updatestock"),
    path('viewbooking/',views.viewbooking,name="viewbooking"),
]