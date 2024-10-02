from django.db.models import Q
from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from datetime import datetime
from django.db import connection

def index(request):
    data=category.objects.all().order_by('-id')[0:6]
    sdata = service_provider.objects.all().order_by('-discount_price')[:]
    md={'cData':data,"servicedata":sdata}

    return render(request,'index.html',md)
def about(request):
    return render(request,'about.html')
def bookHistory(request):
    cursor=connection.cursor()
    email=request.session.get('email')
    cursor.execute("select * from user_tbl_booking left join user_service_provider on user_tbl_booking.provider=user_service_provider.id where user_tbl_booking.email='"+email+"' order by user_tbl_booking.id desc")
    rows=cursor.fetchall()
    md={"data":rows}
    print(rows)
    return render(request,'bookingHistory.html',md)
def bookService(request):
    sId=request.GET.get('msg')
    sdata=service_provider.objects.all().filter(id=sId)
    service_list=services.objects.all().filter(provider_name=sId)
    md={"sdata":sdata,"services":service_list}
    return render(request,'bookService.html',md)
def faq(request):
    return render(request,'FAQs.html')
def myprofile(request):
    user=request.session.get('email')
    data=tbl_register.objects.all().filter(email=user)
    md={"userinfo":data}
    return render(request,'myprofile.html',md)
def login(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        x=tbl_register.objects.filter(email=email,passwd=password)
        if x.count()==1:
            #x[0].name, x[0].picture, x[0].email
            request.session['name']=str(x[0].name)
            request.session['picture']=str(x[0].picture)
            request.session['email']=str(x[0].email)
            return HttpResponse("<script>alert('You are verified');window.location.href='/home/'</script>")
        else:
            return HttpResponse("<script>alert('Invalid Email or Password');window.location.href='/login/'</script>")
    return render(request,'login.html')
def contact(request):
    if request.method=="POST":
        a=request.POST.get('name')
        b=request.POST.get('email')
        c=request.POST.get('mobile')
        d=request.POST.get('msg')
        contactus(Name=a,Email=b,Mobile=c,Message=d).save()
        return HttpResponse("<script>alert('Thanks for Contacting Us');window.location.href='/contact/'</script>")
        #md={"Name":a,"Email":b,"Mobile":c,"Message":d}

    return render(request,'contact.html')
def register(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        mobile=request.POST.get('mobile')
        passwd=request.POST.get('passwd')
        address=request.POST.get('address')
        pincode=request.POST.get('pincode')
        city=request.POST.get('city')
        picture=request.FILES['fu']

        x=tbl_register.objects.all().filter(email=email).count()
        if x==1:
            return HttpResponse("<script>alert('You are already registered');location.href='/home/'</script>")
        else:
            tbl_register(name=name, email=email, mobile=mobile, pincode=pincode, city=city, address=address,passwd=passwd, picture=picture).save()
        return HttpResponse("<script>alert('Thanks for Registering with us');window.location.href='/register/'</script>")

    return render(request,'registration.html')

def logout(request):
    if request.session.get('email'):
        del request.session['email']
        return HttpResponse("<script>alert('You are logged out');window.location.href='/login/'</script>")
    return render(request,'logout.html')


def allservices(request):
    cid=request.GET.get('cid')
    searchdata=request.GET.get('search')
    cdata=category.objects.all().order_by('-id')
    data=""
    if cid is not None:
        data=service_provider.objects.all().filter(service_category=cid)
    elif searchdata is not None:
        data=service_provider.objects.all().filter(Q(service_name__icontains=searchdata)| Q(address__icontains=searchdata)| Q(city__icontains=searchdata) | Q(availability__icontains=searchdata)| Q(service_category__category_name__icontains=searchdata))
    else:
        data = service_provider.objects.all().order_by('-id')
    md={"cdata":cdata,"servicedata":data}
    return render(request,'allServices.html',md)


def booknow(request):
    email=request.session.get('email')
    if email is not None:
        if request.method == "POST":
            date=request.POST.get('date')
            time=request.POST.get('time')
            details=request.POST.get('details')
            address=request.POST.get('address')
            pincode=request.POST.get('pincode')
            city=request.POST.get('city')
            payment=request.POST.get('payment')
            now=datetime.today()
            provider=request.POST.get('provider')
            tbl_booking(provider=provider,email=email,date=date,time=time,details=details,address=address,city=city,pincode=pincode,payment=payment,reqdate=now, status='Pending').save()
            return HttpResponse("<script>alert('Your Booking sent successfully');window.location.href='/booknow/'</script>")
        return render(request,'booknow.html')
    else:
        return HttpResponse("<script>alert('You need to login first, to book service');window.location.href='/login/'</script>")

# Create your views here.
