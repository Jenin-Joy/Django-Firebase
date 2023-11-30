from django.shortcuts import render,redirect
import firebase_admin
from firebase_admin import firestore,credentials,storage,auth
import pyrebase

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
    if 'aid' in request.session:
        return render(request,"Admin/HomePage.html")
    else:
        return redirect("webguest:login")

def logout(request):
    del request.session["aid"]
    return redirect("webguest:login")

def district(request):
    if 'aid' in request.session:
        dis = db.collection("tbl_district").stream()
        district_id = []
        district_name = []
        for i in dis:
            ids = i.id
            data = i.to_dict()
            district_id.append({"id":ids})
            district_name.append(data)
        district = zip(district_id,district_name)
        # print(district)
        if request.method == "POST":
            district = {'district_name':request.POST.get("txt_district")}
            db.collection("tbl_district").add(district)
            return redirect("webadmin:district")
        else:
            return render(request,"Admin/District.html",{'district':district})
    else:
        return redirect("webguest:login")

def deletedistrict(request,id):
    db.collection("tbl_district").document(id).delete()
    return redirect("webadmin:district")

def editdistrict(request,id):
    dis = db.collection("tbl_district").document(id).get()
    data = dis.to_dict()
    if request.method == "POST":
        dis_data = {'district_name':request.POST.get("txt_district")}
        db.collection("tbl_district").document(id).update(dis_data)
        return redirect("webadmin:district")
    # print(data)
    else:
        return render(request,"Admin/District.html",{'dis':data})

def place(request):
    if 'aid' in request.session:
        dis = db.collection("tbl_district").stream()
        dis_data = []
        dis_dict = {}
        for i in dis:
            data = i.to_dict()
            dis_dict = {"data":data,"id":i.id}
            dis_data.append(dis_dict)
        # print(dis_data)


        result = []
        result_dict = {}
        place_data = db.collection("tbl_place").stream()

        for place in place_data:
            place_dict = place.to_dict()
            # district_id = place_dict["district_id"]
            district = db.collection("tbl_district").document(place_dict["district_id"]).get()
            district_dict = district.to_dict()
            result_dict = {'districtdata':district_dict,'placedata':place_dict,'placeid':place.id}
            result.append(result_dict)
        # print(result)

        if request.method == "POST":
            place_data = {'place_name':request.POST.get("txt_place"),'district_id':request.POST.get("sel_district")}
            db.collection("tbl_place").add(place_data)
            return redirect("webadmin:place")
        else:
            return render(request,"Admin/Place.html",{'dis':dis_data,'pla':result})
    else:
        return redirect("webguest:login")

def deleteplace(request,id):
    place = db.collection('tbl_place').document(id).delete()
    return redirect("webadmin:place")

def editplace(request,id):
    dis_data = []
    dis_dict = {}
    dis = db.collection("tbl_district").stream()
    for i in dis:
        data = i.to_dict()
        dis_dict = {"data":data,"id":i.id}
        dis_data.append(dis_dict)
    place = db.collection('tbl_place').document(id).get().to_dict()
    # place_data = place.to_dict()
    if request.method == "POST":
        placedata = {"place_name":request.POST.get("txt_place"),"district_id":request.POST.get("sel_district")} 
        db.collection("tbl_place").document(id).update(placedata)
        return redirect("webadmin:place")
    else:
        return render(request,"Admin/Place.html",{'place':place,'dis':dis_data})

def category(request):
    if 'aid' in request.session:
        cat_data = db.collection("tbl_category").stream()
        cat = []
        for i in cat_data:
            data = {"category":i.to_dict(),"id":i.id}
            cat.append(data)
            # print(cat)
        if request.method =="POST":
            cat = {'category_name':request.POST.get("txt_cat")}
            db.collection("tbl_category").add(cat)
            return redirect("webadmin:category")
        else:
            return render(request,"Admin/Category.html",{'category':cat})
    else:
        return redirect("webguest:login")

def deletecategory(request,id):
    db.collection("tbl_category").document(id).delete()
    return redirect("webadmin:category")

def editcategory(request,id):
    category = db.collection("tbl_category").document(id).get().to_dict()
    if request.method =="POST":
        data = {"category_name":request.POST.get("txt_cat")}
        db.collection("tbl_category").document(id).update(data)
        return redirect("webadmin:category")
    else:
        return render(request,"Admin/Category.html",{'data':category})

def subcategory(request):
    if 'aid' in request.session:
        data = db.collection("tbl_category").stream()
        catdata = []
        for i in data:
            cat = {"cat":i.to_dict(),"id":i.id}
            catdata.append(cat)
            # print(catdata)

        subcat = []
        sub = db.collection("tbl_subcategory").stream()
        for i in sub:
            subcategory = i.to_dict()
            category = db.collection("tbl_category").document(subcategory["category_id"]).get().to_dict()
            subcatdata = {"subcat":subcategory,"category":category,"id":i.id}
            subcat.append(subcatdata)
        # print(subcat)

        if request.method =="POST":
            data = {"subcategory_name":request.POST.get("txt_subcat"),"category_id":request.POST.get("sel_cat")}
            db.collection("tbl_subcategory").add(data)
            return redirect("webadmin:subcategory")
        else:
            return render(request,"Admin/SubCategory.html",{"category":catdata,"subcat":subcat})
    else:
        return redirect("webguest:login")

def deletesubcat(request,id):
    db.collection("tbl_subcategory").document(id).delete()
    return redirect("webadmin:subcategory")

def editsubcat(request,id):
    cate = db.collection("tbl_category").stream()
    cat = []
    for i in cate:
        cat_data = {"cat":i.to_dict(),"id":i.id}
        cat.append(cat_data)
    subcat = db.collection("tbl_subcategory").document(id).get().to_dict()
    # print(subcat)
    if request.method =="POST":
        data = {"subcategory_name":request.POST.get("txt_subcat"),"category_id":request.POST.get("sel_cat")}
        db.collection("tbl_subcategory").document(id).update(data)
        return redirect("webadmin:subcategory")
    else:
        return render(request,"Admin/SubCategory.html",{'category':cat,"subcategory":subcat})

def addsubadmin(request):
    if 'aid' in request.session:
        dis = db.collection("tbl_district").stream()
        district_data = []
        for i in dis:
            data = {"district":i.to_dict(),"id":i.id}
            district_data.append(data)
        subadmin = db.collection("tbl_subadmin").stream()
        suba = []
        for sa in subadmin:
            subadmin = sa.to_dict()
            subdis = subadmin["district_id"]
            district = db.collection("tbl_district").document(subdis).get().to_dict()
            data = {"subadmin":subadmin,"id":sa.id,"district":district} 
            suba.append(data)
        if request.method == "POST":
            email = request.POST.get("txt_email")
            password = request.POST.get("txt_password")
            subadmin = firebase_admin.auth.create_user(email=email,password=password)
            subadmin_image = request.FILES.get("txt_photo")
            if subadmin_image:
                path = "Subadmin/" + subadmin_image.name
                sd.child(path).put(subadmin_image)
                durl = sd.child(path).get_url(None)
            data = {"subadmin_name":request.POST.get("txt_name"),"subadmin_contact":request.POST.get("txt_contact"),"subadmin_email":request.POST.get("txt_email"),"subadmin_address":request.POST.get("txt_address"),"district_id":request.POST.get("sel_district"),"subadmin_photo":durl,"subadmin_id":subadmin.uid}
            db.collection("tbl_subadmin").add(data)
            return redirect("webadmin:addsubadmin")
        else:
            return render(request,"Admin/AddSubadmin.html",{'district':district_data,"sub":suba})
    else:
        return redirect("webguest:login")

def deletesubadmin(request,did):
    subadmin = db.collection("tbl_subadmin").document(did)
    subadmin_data = subadmin.get().to_dict()
    subadmin_id = subadmin_data["subadmin_id"]
    firebase_admin.auth.delete_user(subadmin_id)
    subadmin.delete()
    return redirect("webadmin:addsubadmin")

def viewcomplaint(request):
    if 'aid' in request.session:
        com = db.collection("tbl_complaint").where("subadmin_id", "!=", "0").where("complaint_status", "==", "0").stream()
        com_data = []
        for i in com:
            c = i.to_dict()
            subadmin = db.collection("tbl_subadmin").document(c["subadmin_id"]).get().to_dict()
            com_data.append({"complaint":i.to_dict(),"id":i.id,"subadmin":subadmin})
        return render(request,"Admin/ViewComplaint.html",{"subadmin":com_data})
    else:
        return redirect("webguest:login")

def reply(request,cid):
    if 'aid' in request.session:
        if request.method == "POST":
            db.collection("tbl_complaint").document(cid).update({"complaint_reply":request.POST.get("txt_reply"),"complaint_status":"1"})
            return render(request,"Admin/Reply.html",{"msg":"Reply Sended..."})
        else:
            return render(request,"Admin/Reply.html")
    else:
        return redirect("webguest:login")

def replyedcomplaint(request):
    if 'aid' in request.session:
        com = db.collection("tbl_complaint").where("subadmin_id", "!=", "0").where("complaint_status", "==", "1").stream()
        com_data = []
        for i in com:
            c = i.to_dict()
            subadmin = db.collection("tbl_subadmin").document(c["subadmin_id"]).get().to_dict()
            com_data.append({"complaint":i.to_dict(),"id":i.id,"subadmin":subadmin})
        return render(request,"Admin/ReplyedComplaint.html",{"subadmin":com_data})
    else:
        return redirect("webguest:login")

def viewfeedback(request):
    if 'aid' in request.session:
        user_data = []
        subadmin_data = []
        shop_data = []
        user = db.collection("tbl_feedback").where("user_id", "!=", "0").stream()
        for u in user:
            ufeed = u.to_dict()
            udata = db.collection("tbl_user").document(ufeed["user_id"]).get().to_dict()
            user_data.append({"feedback":u.to_dict(),"id":u.id,"user":udata})
        subadmin = db.collection("tbl_feedback").where("subadmin_id", "!=", "0").stream()
        for sa in subadmin:
            safeed = sa.to_dict()
            subdata = db.collection("tbl_subadmin").document(safeed["subadmin_id"]).get().to_dict()
            subadmin_data.append({"feedback":sa.to_dict(),"id":sa.id,"subadmin":subdata})    
        shop = db.collection("tbl_feedback").where("shop_id", "!=", "0").stream()
        for s in shop:
            sfeed = s.to_dict()
            sdata = db.collection("tbl_shop").document(sfeed["shop_id"]).get().to_dict()
            shop_data.append({"feedback":s.to_dict(),"id":s.id,"shop":sdata})
        return render(request,"Admin/ViewFeedBack.html",{"subadmin":subadmin_data,"shop":shop_data,"user":user_data})
    else:
        return redirect("webguest:login")