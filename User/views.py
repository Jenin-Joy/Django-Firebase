from django.shortcuts import render,redirect
import firebase_admin
from firebase_admin import firestore,credentials,storage,auth
import pyrebase
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from datetime import datetime,timezone
import random
# Create your views here.

db = firestore.client()

def homepage(request):
    user = db.collection("tbl_user").document(request.session["uid"]).get().to_dict()
    # print(user)
    return render(request,"User/HomePage.html",{'user':user})

def profile(request):
    user = db.collection("tbl_user").document(request.session["uid"]).get().to_dict()
    # print(user["user_photo"])
    return render(request,"User/Profile.html",{'user':user})

def editprofile(request):
    data = db.collection("tbl_user").document(request.session["uid"]).get().to_dict()
    if request.method == "POST":
        data = {'user_name':request.POST.get('txt_name'),'user_contact':request.POST.get('txt_contact'),'user_address':request.POST.get('txt_address')}
        db.collection("tbl_user").document(request.session["uid"]).update(data)
        return redirect("webuser:profile")
    else:
        return render(request,"User/EditProfile.html",{'user':data})

def changepassword(request):
    user = db.collection("tbl_user").document(request.session["uid"]).get().to_dict()
    email = user["user_email"]
    # print(email)
    em_link = firebase_admin.auth.generate_password_reset_link(email)
    send_mail(
        'Reset your password ', #subject
        "\rHello \r\nFollow this link to reset your Project password for your " + email + "\n" + em_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your D MARKET team.",#body
        settings.EMAIL_HOST_USER,
        [email],
    )
    return render(request,"User/Profile.html",{"msg":email})

def searchshop(request):
    district = db.collection("tbl_district").stream()
    dis_data = []
    for i in district:
        dis_data.append({"district":i.to_dict(),"id":i.id})
    shop = db.collection("tbl_shop").stream()
    shop_data = []
    for s in shop:
        shop_data.append({"shop":s.to_dict(),"id":s.id})
    return render(request,"User/SearchShop.html",{"dis":dis_data,"shop":shop_data})

def viewproduct(request,shid):
    pdt = db.collection("tbl_product").where("shop_id", "==", shid).stream()
    pdt_data = []
    for i in pdt:
        pdt_data.append({"pdt":i.to_dict(),"id":i.id})
    category = db.collection("tbl_category").stream()
    cat_data = []
    for c in category:
        cat_data.append({"cat":c.to_dict(),"id":c.id})
    return render(request,"User/ViewProduct.html",{"pdt":pdt_data,"cat":cat_data})

def ajaxshop(request):
    shop_data = []
    if request.GET.get("pid") != "":
        shop = db.collection("tbl_shop").where("place_id", "==", request.GET.get("pid")).stream()
        for i in shop:
            shop_data.append({"shop":i.to_dict(),"id":i.id})
    else:
        place = db.collection("tbl_place").where("district_id", "==", request.GET.get("did")).stream()
        for p in place:
            shop = db.collection("tbl_shop").where("place_id", "==", p.id).stream()
            for i in shop:
                shop_data.append({"shop":i.to_dict(),"id":i.id})
    return render(request,"User/AjaxShop.html",{"shop":shop_data})

def ajaxproduct(request):
    pdt_data = []
    if request.GET.get("subcatid") != "":
        pdt = db.collection("tbl_product").where("subcategory_id", "==", request.GET.get("subcatid")).stream()
        for i in pdt:
            pdt_data.append({"pdt":i.to_dict(),"id":i.id})
    else:
        subcat = db.collection("tbl_subcategory").where("category_id", "==", request.GET.get("catid")).stream()
        for s in subcat:
            pdt = db.collection("tbl_product").where("subcategory_id", "==", s.id).stream()
            for i in pdt:
                pdt_data.append({"pdt":i.to_dict(),"id":i.id})
    return render(request,"User/AjaxProduct.html",{"pdt":pdt_data})

def addtocart(request,pid):
    cartcount = ""
    bookcount = ""
    bid = ""
    book = db.collection("tbl_booking").where("booking_status", "==", "0").where("user_id", "==", request.session["uid"]).stream()
    for bk in book:
        bookcount = bk.to_dict()
        bid = bk.id
    if bookcount:
        cart = db.collection("tbl_cart").where("product_id", "==", pid).where("booking_id", "==", bid).stream()
        for ct in cart:
            cartcount = ct.to_dict()
        if cartcount:
            return render(request,"User/ViewProduct.html",{"msg":"Product Already added to cart"})
        else:
            db.collection("tbl_cart").add({"cart_qty":"1","cart_status":"0","product_id":pid,"booking_id":bid})
            return render(request,"User/ViewProduct.html",{"msg":"Product added to cart"})
    else:
        db.collection("tbl_booking").add({"booking_status":"0","user_id":request.session["uid"],"booking_date":firestore.SERVER_TIMESTAMP})
        book = db.collection("tbl_booking").where("booking_status", "==", "0").where("user_id", "==", request.session["uid"]).stream()
        for bk in book:
            bookcount = bk.to_dict()
            bid = bk.id
        if bookcount:
            cart = db.collection("tbl_cart").where("product_id", "==", pid).where("booking_id", "==", bid).stream()
            for ct in cart:
                cartcount = ct.to_dict()
            if cartcount:
                return render(request,"User/ViewProduct.html",{"msg":"Product Already added to cart"})
            else:
                db.collection("tbl_cart").add({"cart_qty":"1","cart_status":"0","product_id":pid,"booking_id":bid})
                return render(request,"User/ViewProduct.html",{"msg":"Product added to cart"})
        else:
            return render(request,"User/ViewProduct.html")

def mycart(request):
    bkid = ""
    booking = db.collection("tbl_booking").where("user_id", "==", request.session["uid"]).where("booking_status", "==", "0").stream()
    for b in booking:
        bkid = b.id
    cart = db.collection("tbl_cart").where("booking_id", "==", bkid).stream()
    cart_data = []
    tot = 0
    length = 0
    for c in cart:
        ca = c.to_dict()
        pdt = db.collection("tbl_product").document(ca["product_id"]).get().to_dict()
        cart_data.append({"cart":ca,"id":c.id,"product":pdt})
        length =length + len(ca)
        tot = tot + int(ca["cart_qty"]) * int(pdt["product_rate"])
    # print(cart_data)
    count = int(length/4)
    if request.method == "POST":
        return redirect("webuser:payment")
    else:
        return render(request,"User/MyCart.html",{"cart":cart_data,"count":count,"total":tot})

def deletecartitem(request,cid):
    db.collection("tbl_cart").document(cid).delete()
    return render(request,"User/MyCart.html",{"msg":"Item Deleted form the cart"})

def ajaxmycart(request):
    cart_data = []
    db.collection("tbl_cart").document(request.GET.get("cartid")).update({"cart_qty":request.GET.get("qty")})
    return render(request,"User/AjaxCart.html")

def payment(request):
    bkid = ""
    booking = db.collection("tbl_booking").where("user_id", "==", request.session["uid"]).where("booking_status", "==", "0").stream()
    for b in booking:
        bkid = b.id
    cart = db.collection("tbl_cart").where("booking_id", "==", bkid).stream()
    cart_data = []
    tot = 0
    length = 0
    for c in cart:
        ca = c.to_dict()
        pdt = db.collection("tbl_product").document(ca["product_id"]).get().to_dict()
        tot = tot + int(ca["cart_qty"]) * int(pdt["product_rate"])

    if request.method == "POST":
        cart = db.collection("tbl_cart").where("booking_id", "==", bkid).stream()
        for c in cart:
            ct = c.to_dict()
            pdt = db.collection("tbl_product").document(ct["product_id"]).get().to_dict()
            qty = ct["cart_qty"]
            stock = pdt["product_qty"]
            balance = int(stock) - int(qty)
            db.collection("tbl_product").document(ct["product_id"]).update({"product_qty":balance})
        db.collection("tbl_booking").document(bkid).update({"booking_status":"1"})
        return redirect("webuser:loader")
    else:
        return render(request,"User/Payment.html",{"total":tot})

def paymentsuc(request):
    return render(request,"User/Payment_suc.html")

def loader(request):
    return render(request,"User/Loader.html")

def mybooking(request):
    book_data = []
    book = db.collection("tbl_booking").where("user_id", "==", request.session["uid"]).where("booking_status", "==", "1").stream()
    for b in book:
        cart_data  = db.collection("tbl_cart").where("booking_id", "==", b.id).stream()
        tot = 0
        for c in cart_data:
            crt = c.to_dict()
            # print(crt)
            pro = db.collection("tbl_product").document(crt["product_id"]).get().to_dict()
            tot = tot + int(crt["cart_qty"]) * int(pro["product_rate"])
        # print(tot)
        data = {"book":b.to_dict(),"id":b.id,"total":tot}
        book_data.append(data)
    return render(request,"User/MyBooking.html",{'book':book_data})

def bookedproducts(request,id):
    cart = db.collection("tbl_cart").where("booking_id", "==", id).stream()
    cart_data = []
    for c in cart:
        ct = c.to_dict()
        pdt = db.collection("tbl_product").document(ct["product_id"]).get().to_dict()
        cart_data.append({"cart":ct,"product":pdt})
    return render(request,"User/MyBookedPdt.html",{"cart":cart_data,"id":id})

def bills(request,id):
    cart_data = []
    user = db.collection("tbl_user").document(request.session["uid"]).get().to_dict()
    book = db.collection("tbl_booking").document(id).get().to_dict()
    cart = db.collection("tbl_cart").where("booking_id", "==", id).stream()
    rand=random.randint(111111,999999)
    tot = 0
    for c in cart:
        ca = c.to_dict()
        pdt = db.collection("tbl_product").document(ca["product_id"]).get().to_dict()
        shop = db.collection("tbl_shop").document(pdt["shop_id"]).get().to_dict()
        cart_data.append({"cart":ca,"id":c.id,"product":pdt,"shop":shop})
        tot = tot + int(ca["cart_qty"]) * int(pdt["product_rate"])
    return render(request,"User/Bills.html",{"user":user,"tot":tot,"booking":book,"ran":rand,"bill":cart_data})