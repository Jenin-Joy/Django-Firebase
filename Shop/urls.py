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
    path('vieworderpdt/<str:id>',views.vieworderpdt,name="vieworderpdt"),
    path('itemdelivered/<str:id>',views.itemdelivered,name="itemdelivered"),
    path('complaint/',views.complaint,name="complaint"),
    path('viewreply/',views.viewreply,name="viewreply"),
    path('feedback/',views.feedback,name="feedback"),
    path('logout/',views.logout,name="logout"),
]