from django.urls import path,include
from Subadmin import views
app_name="websubadmin"
urlpatterns = [
    path('home/',views.home,name="home"),
    path('profile/',views.profile,name="profile"),
    path('changepassword/',views.changepassword,name="changepassword"),
    path('editprofile/',views.editprofile,name="editprofile"),
    path('newshop/',views.newshop,name="newshop"),
    path('acceptshop/<str:acid>',views.acceptshop,name="acceptshop"),
    path('rejectshop/<str:rjid>',views.rejectshop,name="rejectshop"),
    path('acceptedshop/',views.acceptedshop,name="acceptedshop"),
    path('rejectedshop/',views.rejectedshop,name="rejectedshop"),
    path('newuser/',views.newuser,name="newuser"),
    path('viewcomplaint/',views.viewcomplaint,name="viewcomplaint"),
    path('reply/<str:cid>',views.reply,name="reply"),
    path('replyedcomplaint/',views.replyedcomplaint,name="replyedcomplaint"),
    path('complaint/',views.complaint,name="complaint"),
    path('viewreply/',views.viewreply,name="viewreply"),
    path('feedback/',views.feedback,name="feedback"),
    path('logout/',views.logout,name="logout"),
]