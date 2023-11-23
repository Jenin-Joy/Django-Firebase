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
auth = firebase.auth()
sd = firebase.storage()

def home(request):
    shop = db.collection("tbl_shop").document(request.session["shid"]).get().to_dict()
    return render(request,"Shop/HomePage.html",{'shop':shop})

def profile(request):
    shop = db.collection("tbl_shop").document(request.session["shid"]).get().to_dict()
    return render(request,"Shop/Profile.html",{'shop':shop})

def editprofile(request):
    shop = db.collection("tbl_shop").document(request.session["shid"]).get().to_dict()
    if request.method == "POST":
        db.collection("tbl_shop").document(request.session["shid"]).update({'shop_name':request.POST.get("txt_name"),'shop_contact':request.POST.get("txt_contact"),'shop_address':request.POST.get("txt_address")})
        return render(request,"Shop/EditProfile.html",{"msg":"Profile Updated"})
    else:
        return render(request,"Shop/EditProfile.html",{'shop':shop})

def changepassword(request):
    shop = db.collection("tbl_shop").document(request.session["shid"]).get().to_dict()
    email = shop["shop_email"]
    em_link = firebase_admin.auth.generate_password_reset_link(email)
    send_mail(
        'Reset your password ', #subject
        "\rHello \r\nFollow this link to reset your Project password for your " + email + "\n" + em_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your D MARKET team.",#body
        settings.EMAIL_HOST_USER,
        [email],
    )
    return render(request,"Shop/Profile.html",{"msg":email})

def addproduct(request):
    cat = db.collection("tbl_category").stream()
    cat_data = []
    for i in cat:
        data = {"category":i.to_dict(),"id":i.id}
        cat_data.append(data)
    pdt = db.collection("tbl_product").where("shop_id", "==", request.session["shid"]).stream()
    pdt_data = []
    for p in pdt:
        pdtdata = p.to_dict()
        subcat = db.collection("tbl_subcategory").document(pdtdata["subcategory_id"]).get().to_dict()
        cat = db.collection("tbl_category").document(subcat["category_id"]).get().to_dict()
        data = {"product":pdtdata,"subcat":subcat,"cat":cat,"id":p.id}
        pdt_data.append(data)
    if request.method == "POST":
        photo = request.FILES.get("txt_photo")
        if photo:
            path = "Shop/Product/" + photo.name
            sd.child(path).put(photo)
            durl = sd.child(path).get_url(None)
        db.collection("tbl_product").add({"product_name":request.POST.get("txt_pdtname"),"product_rate":request.POST.get("txt_rate"),"product_qty":request.POST.get("txt_qty"),"subcategory_id":request.POST.get("sel_subcategory"),"shop_id":request.session["shid"],"product_photo":durl})
        return render(request,"Shop/AddProduct.html",{"msg":"Producted Added"})
    else:
        return render(request,"Shop/AddProduct.html",{'cat':cat_data,'product':pdt_data})

def ajaxsubcategory(request):
    subcat = db.collection("tbl_subcategory").where("category_id", "==", request.GET.get("catid")).stream()
    subcat_data = []
    for i in subcat:
        data = {"subcat":i.to_dict(),"id":i.id}
        subcat_data.append(data)
    return render(request,"Shop/AjaxSubcategory.html",{'subcat':subcat_data})

def deleteproduct(request,did):
    db.collection("tbl_product").document(did).delete()
    return render(request,"Shop/AddProduct.html",{'msg':"Product Deleted"})

def updatestock(request,pid):
    if request.method == "POST":
        pdt = db.collection("tbl_product").document(pid).get().to_dict()
        pdt_oldqty = pdt["product_qty"]
        new_qty = int(pdt_oldqty) + int(request.POST.get("txt_qty"))
        db.collection("tbl_product").document(pid).update({"product_qty":new_qty})
        return render(request,"Shop/AddStock.html",{"msg":"Stock Updated"})
    else:
        return render(request,"Shop/AddStock.html")

def viewbooking(request):
    book_data = []
    bkid = []
    pdt = db.collection("tbl_product").where("shop_id", "==", request.session["shid"]).stream()
    for p in pdt:
        cart = db.collection("tbl_cart").where("product_id", "==", p.id).stream()
        for c in cart:
            ct = c.to_dict()
            bkid.append(ct["booking_id"])
    book = db.collection("tbl_booking").where("id", "==", bkid).stream()
    for b in book:
        print(b.to_dict())
    return render(request,"Shop/ViewBooking.html",{'book':book_data})

    