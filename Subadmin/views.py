from django.shortcuts import render,redirect
import firebase_admin
from firebase_admin import firestore,credentials,storage,auth
import pyrebase
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from datetime import date
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
    if 'said' in request.session:
        subadmin = db.collection("tbl_subadmin").document(request.session["said"]).get().to_dict()
        return render(request,"Subadmin/HomePage.html",{'data':subadmin})
    else:
        return redirect("webguest:login")

def logout(request):
    del request.session["said"]
    return redirect("webguest:login")

def profile(request):
    if 'said' in request.session:
        subadmin = db.collection("tbl_subadmin").document(request.session["said"]).get().to_dict()
        return render(request,"Subadmin/Profile.html",{"subadmin":subadmin})
    else:
        return redirect("webguest:login")

def changepassword(request):
    if 'said' in request.session:
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
    else:
        return redirect("webguest:login")

def editprofile(request):
    if 'said' in request.session:
        subadmin = db.collection("tbl_subadmin").document(request.session["said"]).get().to_dict()
        if request.method == "POST":
            data = {"subadmin_name":request.POST.get("txt_name"),"subadmin_contact":request.POST.get("txt_contact"),"subadmin_address":request.POST.get("txt_address")}
            db.collection("tbl_subadmin").document(request.session["said"]).update(data)
            return render(request,"Subadmin/EditProfile.html",{"msg":1})
        return render(request,"Subadmin/EditProfile.html",{"subadmin":subadmin})
    else:
        return redirect("webguest:login")

def newshop(request):
    if 'said' in request.session:
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
    else:
        return redirect("webguest:login")

def acceptedshop(request):
    if 'said' in request.session:
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
    else:
        return redirect("webguest:login")

def rejectedshop(request):
    if 'said' in request.session:
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
    else:
        return redirect("webguest:login")

def acceptshop(request,acid):
    db.collection("tbl_shop").document(acid).update({"shop_status":"1"})
    return redirect("websubadmin:home")

def rejectshop(request,rjid):
    db.collection("tbl_shop").document(rjid).update({"shop_status":"2"})
    return redirect("websubadmin:home")

def newuser(request):
    if 'said' in request.session:
        placedata = db.collection("tbl_place").where("district_id", "==", request.session["subdis"]).stream()
        user_data = []
        for p in placedata:
            user = db.collection("tbl_user").where("place_id", "==", p.id).stream()
            for i in user:
                user = i.to_dict()
                place = db.collection("tbl_place").document(user["place_id"]).get().to_dict()
                district = db.collection("tbl_district").document(place["district_id"]).get().to_dict()
                data = {"user":i.to_dict(),"id":i.id,"district":district,"place":place}
                user_data.append(data)
        return render(request,"Subadmin/NewUser.html",{"user":user_data})
    else:
        return redirect("webguest:login")

def viewcomplaint(request):
    if 'said' in request.session:
        placedata = db.collection("tbl_place").where("district_id", "==", request.session["subdis"]).stream()
        user_data = []
        shop_data = []
        for p in placedata:
            user = db.collection("tbl_user").where("place_id", "==", p.id).stream()
            for u in user:
                com = db.collection("tbl_complaint").where("user_id", "==", u.id).where("complaint_status", "==", "0").stream()
                for c in com:
                    user_data.append({"complaint":c.to_dict(),"id":c.id,"user":u.to_dict()})
            shop = db.collection("tbl_shop").where("place_id", "==", p.id).stream()
            for s in shop:
                com = db.collection("tbl_complaint").where("shop_id", "==", s.id).where("complaint_status", "==", "0").stream()
                for c in com:
                    shop_data.append({"complaint":c.to_dict(),"id":c.id,"shop":s.to_dict()})
        return render(request,"Subadmin/ViewComplaint.html",{"user":user_data,"shop":shop_data})
    else:
        return redirect("webguest:login")

def reply(request,cid):
    if 'said' in request.session:
        if request.method == "POST":
            db.collection("tbl_complaint").document(cid).update({"complaint_reply":request.POST.get("txt_reply"),"complaint_status":"1"})
            return render(request,"Subadmin/Reply.html",{"msg":"Reply Sended..."})
        else:
            return render(request,"Subadmin/Reply.html")
    else:
        return redirect("webguest:login")

def replyedcomplaint(request):
    if 'said' in request.session:
        placedata = db.collection("tbl_place").where("district_id", "==", request.session["subdis"]).stream()
        user_data = []
        shop_data = []
        for p in placedata:
            user = db.collection("tbl_user").where("place_id", "==", p.id).stream()
            for u in user:
                com = db.collection("tbl_complaint").where("user_id", "==", u.id).where("complaint_status", "==", "1").stream()
                for c in com:
                    user_data.append({"complaint":c.to_dict(),"id":c.id,"user":u.to_dict()})
            shop = db.collection("tbl_shop").where("place_id", "==", p.id).stream()
            for s in shop:
                com = db.collection("tbl_complaint").where("shop_id", "==", s.id).where("complaint_status", "==", "1").stream()
                for c in com:
                    shop_data.append({"complaint":c.to_dict(),"id":c.id,"shop":s.to_dict()})
        return render(request,"Subadmin/ReplyedComplaint.html",{"user":user_data,"shop":shop_data})
    else:
        return redirect("webguest:login")

def complaint(request):
    if 'said' in request.session:
        if request.method == "POST":
            datedata = date.today()
            db.collection("tbl_complaint").add({"complaint_content":request.POST.get("txt_complaint"),"subadmin_id":request.session["said"],"complaint_status":"0","complaint_date":str(datedata),"complaint_reply":""})
            return render(request,"Subadmin/Complaint.html",{"msg":"complaint sended.."})
        else:
            return render(request,"Subadmin/Complaint.html")
    else:
        return redirect("webguest:login")

def viewreply(request):
    if 'said' in request.session:
        com = db.collection("tbl_complaint").where("subadmin_id", "==", request.session["said"]).stream()
        com_data = []
        for c in com:
            com_data.append({"complaint":c.to_dict(),"id":c.id})
        return render(request,"Subadmin/ViewReply.html",{"com":com_data})
    else:
        return redirect("webguest:login")

def feedback(request):
    if 'said' in request.session:
        if request.method == "POST":
            db.collection("tbl_feedback").add({"feedback_content":request.POST.get("txt_feedback"),"subadmin_id":request.session["said"]})
            return render(request,"Subadmin/FeedBack.html",{"msg":"FeedBack Sended.."})
        else:
            return render(request,"Subadmin/FeedBack.html")
    else:
        return redirect("webguest:login")