from django.shortcuts import render,redirect
import firebase_admin
from firebase_admin import firestore,credentials,storage,auth
import pyrebase
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

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
auth = firebase.auth()
sd = firebase.storage()

# Create your views here.

def index(request):
    return render(request,"Guest/index.html")

def userreg(request):
    district_data = []
    district_result = {}
    district = db.collection("tbl_district").stream()
    for i in district:
        data = i.to_dict()
        district_result = {"data":data,"id":i.id}
        district_data.append(district_result)
    if request.method == "POST":
        email = request.POST.get("txt_email")
        password = request.POST.get("txt_password")
        try:
            user = firebase_admin.auth.create_user(email=email,password=password)
        except (firebase_admin._auth_utils.EmailAlreadyExistsError,ValueError) as error:
            # print(error)
            return render(request,"Guest/CustomerReg.html",{"msg":error})
        # print(user.uid)
        image = request.FILES.get("txt_photo")
        if image:
            path = "User/" + image.name
            sd.child(path).put(image)
            download_url = sd.child(path).get_url(None)
        user = {"user_id":user.uid,"user_name":request.POST.get("txt_name"),"user_contact":request.POST.get("txt_contact"),"user_email":request.POST.get("txt_email"),"user_address":request.POST.get("txt_address"),"place_id":request.POST.get("sel_place"),"user_photo":download_url}
        db.collection("tbl_user").document().set(user)
        return render(request,"Guest/CustomerReg.html",{"msg":"Account Created"})
    else:
        return render(request,"Guest/CustomerReg.html",{"district":district_data})

def ajaxplace(request):
    place = db.collection("tbl_place").where("district_id" ,"==" ,request.GET.get("disd")).stream()
    place_data = {}
    place_result = []
    for p in place:
        place_data = {"place":p.to_dict(),"id":p.id}
        place_result.append(place_data)
    # print(place_result)
    return render(request,"Guest/Ajaxplace.html",{"place":place_result})

def login(request):
    udata_id = ""
    subadmindata_id = ""
    shopdata_id = ""
    if request.method == "POST":
        email = request.POST.get("txt_email")
        password = request.POST.get("txt_password")
        if (email == "admin@gmail.com") & (password == "itsmeadmin"):
            request.session["aid"] = 1
            return redirect("webadmin:home")
        else:
            try:
                user = auth.sign_in_with_email_and_password(email,password)
            except: 
                return render(request,"Guest/Login.html",{'msg':"INVALID_LOGIN_CREDENTIALS... Check Email and Password"})
            userid = user["localId"]
            user_data = db.collection("tbl_user").where("user_id", "==", userid).stream()
            for i in user_data:
                udata_id = i.id
            subadmin_data = db.collection("tbl_subadmin").where("subadmin_id", "==", userid).stream()
            for sa in subadmin_data:
                subadmindata_id = sa.id
                sub = sa.to_dict()
                sub_dis = sub["district_id"] 
            shop_data = db.collection("tbl_shop").where("shop_id", "==", userid).stream()
            for shop in shop_data:
                shopdata_id = shop.id
                shop_data = shop.to_dict()
                shop_status = shop_data["shop_status"]
            if udata_id:
                request.session["uid"] = udata_id
                return redirect("webuser:homepage")
            elif subadmindata_id:
                request.session["said"] = subadmindata_id
                request.session["subdis"] = sub_dis
                return redirect("websubadmin:home")
            elif shopdata_id:
                if shop_status == "2":
                    return render(request,"Guest/Login.html",{"msg":"Your Request is Rejected"})
                elif shop_status == "0":
                    return render(request,"Guest/Login.html",{"msg":"Your Request is Pending"})
                else:
                    request.session["shid"] = shopdata_id
                    return redirect("webshop:home")
            else:
                # print(udata_id)
                return render(request,"Guest/Login.html",{"msg":"Your Request is pending or Rejected"})
    else:
        return render(request,"Guest/Login.html")

# def example(request):
    if request.method == "POST":
        image = request.FILES.get("txt_photo")
        # bucket = storage.bucket()
        # blob = bucket.blob("Example/" + photo.name)
        # blob.upload_from_file(photo.file)
        # download_url = get_url(blob)
        # print(download_url)
        # if image:
        #     path = "Example/" + image.name
        #     sd.child(path).put(image)
        #     download_url = sd.child(path).get_url(None)
        #     print(download_url)
            # ima = {'image':download_url}
            # db.child("photo").push(ima)
        return render(request,"Guest/Example.html")
    else:
        return render(request,"Guest/Example.html")

# def example(request):
    if request.method == "POST":
        email = request.POST.get("txt_email")
        em = firebase_admin.auth.generate_password_reset_link(email)
        # print(em)
        send_mail(
            'Reset your password ', #subject
            "\rHello \r\nFollow this link to reset your Project password for your " + email + "\n" + em +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your D MARKET team.",#body
            settings.EMAIL_HOST_USER,
            [email],

        )
        return render(request,"Guest/Example.html",{"msg":email})
    else:
        return render(request,"Guest/Example.html")

# def example(request):
    # if request.method == "POST":
    #     data = {"example_data":request.POST.get("txt_example")}
    #     sample.collections("tbl_example").add(data)
    #     return redirect("webguest:example")
    # else:
    # return render(request,"Guest/Example.html")

# def ajaxexample(request):
    return render(request,"Guest/ajaxexample.html")

def shopreg(request):
    district = db.collection("tbl_district").stream()
    dis_data = []
    for i in district:
        dis = {"district":i.to_dict(),"id":i.id}
        dis_data.append(dis)
    if request.method == "POST":
        email = request.POST.get("txt_email")
        password = request.POST.get("txt_password")

        try:
            shop = firebase_admin.auth.create_user(email=email,password=password)
        except (firebase_admin._auth_utils.EmailAlreadyExistsError,ValueError) as error:
            return render(request,"Guest/ShopReg.html",{"msg":error})
        photo = request.FILES.get("txt_photo")
        if photo:
            photo_path =  "Shop/Photo/" + photo.name
            sd.child(photo_path).put(photo)
            photo_url = sd.child(photo_path).get_url(None)
        proof = request.FILES.get("txt_proof")
        if proof:
            proof_path = "Shop/proof/" + proof.name
            sd.child(proof_path).put(proof)
            proof_url = sd.child(proof_path).get_url(None)
        data = {"shop_id":shop.uid,"shop_name":request.POST.get("txt_name"),"shop_contact":request.POST.get("txt_contact"),"shop_email":request.POST.get("txt_email"),"shop_address":request.POST.get("txt_address"),"place_id":request.POST.get("sel_place"),"shop_photo":photo_url,"shop_proof":proof_url,"shop_status":0}
        db.collection("tbl_shop").add(data)
        return render(request,"Guest/ShopReg.html",{"msg":"Account Created Sucessfully.."})
    else:
        return render(request,"Guest/ShopReg.html",{'dis':dis_data})