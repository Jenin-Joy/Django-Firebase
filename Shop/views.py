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
    tot_data = []
    bkid = set()
    pdt = db.collection("tbl_product").where("shop_id", "==", request.session["shid"]).stream()
    for p in pdt:
        cart = db.collection("tbl_cart").where("product_id", "==", p.id).stream()
        for c in cart:
            ct = c.to_dict()
            bkid.add(ct["booking_id"])
    for bk in bkid:
        book = db.collection("tbl_booking").document(bk).get().to_dict()
        if book["booking_status"] >= "1":
            user = db.collection("tbl_user").document(book["user_id"]).get().to_dict()
            book_data.append({"book":book,"user":user,"id":bk})
    for data in book_data:
        cart_data  = db.collection("tbl_cart").where("booking_id", "==", data['id']).where("cart_status", "==", "0").stream()
        tot = 0
        for c in cart_data:
            crt = c.to_dict()
            # print(crt)
            pro = db.collection("tbl_product").document(crt["product_id"]).get().to_dict()
            tot = tot + int(crt["cart_qty"]) * int(pro["product_rate"])
        # print(tot)
        tot_data.append({"total":tot})
    final_data = zip(book_data,tot_data)
    return render(request,"Shop/ViewBooking.html",{'book':final_data})

def vieworderpdt(request,id):
    cart = db.collection("tbl_cart").where("booking_id", "==", id).where("cart_status", "==", "0").stream()
    cart_pdt = []
    for c in cart:
        ct = c.to_dict()
        pdt = db.collection("tbl_product").document(ct["product_id"]).get().to_dict()
        cart_pdt.append({"cart":ct,"id":c.id,"product":pdt})
    return render(request,"Shop/ViewOrderProduct.html",{"data":cart_pdt})

def itemdelivered(request,id):
    db.collection("tbl_booking").document(id).update({"booking_status":"3"})
    return render(request,"Shop/ViewBooking.html",{"msg":"Item Delivered"})

def complaint(request):
    if request.method == "POST":
        datedata = date.today()
        db.collection("tbl_complaint").add({"complaint_content":request.POST.get("txt_complaint"),"shop_id":request.session["shid"],"complaint_status":"0","complaint_date":str(datedata),"complaint_reply":""})
        return render(request,"Shop/HomePage.html",{"msg":"complaint sended.."})
    else:
        return render(request,"Shop/Complaint.html")

def viewreply(request):
    com = db.collection("tbl_complaint").where("shop_id", "==", request.session["shid"]).stream()
    com_data = []
    for c in com:
        com_data.append({"complaint":c.to_dict(),"id":c.id})
    return render(request,"Shop/ViewReply.html",{"com":com_data})