from django.shortcuts import render,redirect
import firebase_admin
from firebase_admin import firestore,credentials,storage,auth
import pyrebase
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
# Create your views here.

db = firestore.client()
config = {
    "apiKey": "AIzaSyDvUX03ibtlX4w0jLtPaDFFREDcOAZj7hs",
    "authDomain": "django-firebase-6a58d.firebaseapp.com",
    "projectId": "django-firebase-6a58d",
    "storageBucket": "django-firebase-6a58d.appspot.com",
    "messagingSenderId": "186665879224",
    "appId": "1:186665879224:web:86ef1f66e2484a8409d64d",
    "measurementId": "G-51W27JBRB7",
    "databaseURL":""
}

firebase = pyrebase.initialize_app(config)

def home(request):
    subadmin = db.collection("tbl_subadmin").document(request.session["said"]).get().to_dict()
    return render(request,"Subadmin/HomePage.html",{'data':subadmin})

def profile(request):
    subadmin = db.collection("tbl_subadmin").document(request.session["said"]).get().to_dict()
    return render(request,"Subadmin/Profile.html",{"subadmin":subadmin})

def changepassword(request):
    subadmin = db.collection("tbl_subadmin").document(request.session["said"]).get().to_dict()
    subadmin_email = subadmin["subadmin_email"]
    em_link = firebase_admin.auth.generate_password_reset_link(subadmin_email)
    send_mail(
        'Reset your password ', #subject
        "\rHello \r\nFollow this link to reset your Project password for your " + email + "\n" + em_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your D MARKET team.",#body
        settings.EMAIL_HOST_USER,
        [email],
    )
    return render(request,"Subadmin/Profile.html",{"msg":subadmin_email})

def editprofile(request):
    subadmin = db.collection("tbl_subadmin").document(request.session["said"]).get().to_dict()
    if request.method == "POST":
        data = {"subadmin_name":request.POST.get("txt_name"),"subadmin_contact":request.POST.get("txt_contact"),"subadmin_address":request.POST.get("txt_address")}
        db.collection("tbl_subadmin").document(request.session["said"]).update(data)
        return render(request,"Subadmin/EditProfile.html",{"msg":1})
    return render(request,"Subadmin/EditProfile.html",{"subadmin":subadmin})

def newshop(request):
    place = db.collection("tbl_place").where("district_id", "==", request.session["subdis"]).stream()
    for p in place:
        shop = db.collection("tbl_shop").where("shop_status", "==", "0").where("place_id", "==", p.id).stream()
        shop_data = []
        for i in shop:
            shop = i.to_dict()
            place = db.collection("tbl_place").document(shop["place_id"]).get().to_dict()
            district = db.collection("tbl_district").document(place["district_id"]).get().to_dict()
            data = {"shop":i.to_dict(),"id":i.id,"district":district,"place":place}
            shop_data.append(data)
    return render(request,"Subadmin/NewShop.html",{'shop':shop_data})

def acceptedshop(request):
    place = db.collection("tbl_place").where("district_id", "==", request.session["subdis"]).stream()
    for p in place:
        shop = db.collection("tbl_shop").where("shop_status", "==", "1").where("place_id", "==", p.id).stream()
        shop_data = []
        for i in shop:
            shop = i.to_dict()
            place = db.collection("tbl_place").document(shop["place_id"]).get().to_dict()
            district = db.collection("tbl_district").document(place["district_id"]).get().to_dict()
            data = {"shop":i.to_dict(),"id":i.id,"district":district,"place":place}
            shop_data.append(data)
    return render(request,"Subadmin/AcceptedShop.html",{'shop':shop_data})

def rejectedshop(request):
    place = db.collection("tbl_place").where("district_id", "==", request.session["subdis"]).stream()
    for p in place:
        shop = db.collection("tbl_shop").where("shop_status", "==", "2").where("place_id", "==", p.id).stream()
        shop_data = []
        for i in shop:
            shop = i.to_dict()
            place = db.collection("tbl_place").document(shop["place_id"]).get().to_dict()
            district = db.collection("tbl_district").document(place["district_id"]).get().to_dict()
            data = {"shop":i.to_dict(),"id":i.id,"district":district,"place":place}
            shop_data.append(data)
    return render(request,"Subadmin/RejectedShop.html",{'shop':shop_data})

def acceptshop(request,acid):
    db.collection("tbl_shop").document(acid).update({"shop_status":"1"})
    return redirect("websubadmin:home")

def rejectshop(request,rjid):
    db.collection("tbl_shop").document(rjid).update({"shop_status":"2"})
    return redirect("websubadmin:home")

def newuser(request):
    user = db.collection("tbl_user").stream()
    user_data = []
    for i in user:
        user = i.to_dict()
        place = db.collection("tbl_place").document(user["place_id"]).get().to_dict()
        district = db.collection("tbl_district").document(place["district_id"]).get().to_dict()
        data = {"user":i.to_dict(),"id":i.id,"district":district,"place":place}
        user_data.append(data)
    return render(request,"Subadmin/NewUser.html",{"user":user_data})