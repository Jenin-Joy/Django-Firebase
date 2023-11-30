from django.urls import path,include
from Guest import views
app_name="webguest"

urlpatterns = [
    path('userreg/',views.userreg,name="userreg"),
    path('ajaxplace/',views.ajaxplace,name="ajaxplace"),
    path('login/',views.login,name="login"),
    # path('example/',views.example,name="example"),
    path('shopreg/',views.shopreg,name="shopreg"),
    path('',views.index,name="index"),
    # path('ajaxexample/',views.ajaxexample,name="ajaxexample"),
]