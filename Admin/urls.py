from django.urls import path,include
from Admin import views
app_name="webadmin"

urlpatterns = [
    path('home/',views.home,name="home"),
    path('district/',views.district,name="district"),
    path('deletedistrict/<str:id>',views.deletedistrict,name="deletedistrict"),
    path('editdistrict/<str:id>',views.editdistrict,name="editdistrict"),
    path('place/',views.place,name="place"),
    path('deleteplace/<str:id>',views.deleteplace,name="deleteplace"),
    path('editplace/<str:id>',views.editplace,name="editplace"),
    path('category/',views.category,name="category"),
    path('deletecategory/<str:id>',views.deletecategory,name="deletecategory"),
    path('editcategory/<str:id>',views.editcategory,name="editcategory"),
    path('subcategory/',views.subcategory,name="subcategory"),
    path('deletesubcat/<str:id>',views.deletesubcat,name="deletesubcat"),
    path('editsubcat/<str:id>',views.editsubcat,name="editsubcat"),
    path('addsubadmin/',views.addsubadmin,name="addsubadmin"),
    path('deletesubadmin/<str:did>',views.deletesubadmin,name="deletesubadmin"),
    path('viewcomplaint/',views.viewcomplaint,name="viewcomplaint"),
    path('reply/<str:cid>',views.reply,name="reply"),
    path('replyedcomplaint/',views.replyedcomplaint,name="replyedcomplaint"),
    path('viewfeedback/',views.viewfeedback,name="viewfeedback"),
    path('logout/',views.logout,name="logout"),
]