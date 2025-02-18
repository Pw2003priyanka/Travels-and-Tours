from typing import Any
from django.shortcuts import render,redirect, get_object_or_404
from .models import package,customer,travel_agency,cart,order,payment,orderdetail
from django.http import HttpResponse
from django.views.generic import DeleteView,ListView,CreateView,UpdateView,DetailView
from django.db.models import Q
from django.contrib.auth.hashers import make_password,check_password
from django.template import loader
from datetime import date
from django.core.mail import EmailMessage
from django.urls import reverse_lazy

# Create your views here.
class packageview(ListView):
    model=package
    template_name='packageview.html'
    context_object_name='pacobj'

    def get_context_data(self, **kwargs):
        data = self.request.session['sessionvalue']
        context = super().get_context_data(**kwargs)
        context['session'] = data
        return context

    def package_view(request):
        if request.method=="GET":
            return render(request,'packageview.html')
        
def search(request):
    if request.method=="POST":
        searchdata=request.POST.get('searchquery')
        pacobj=package.objects.filter(Q(package_name__icontains=searchdata) | Q(package_price__icontains=searchdata))
        return render(request,'packageview.html',{'pacobj':pacobj})
    
class packagedetail(DetailView):
    model=package
    template_name="packagedetail.html"
    context_object_name="d"


class travel_agencyview(ListView):
    model=travel_agency
    template_name='index.html'
    context_object_name='travobj'

    def travel_agencyview(request):
        if request.method == "GET" :
            return render(request, 'index.html')
    

def register(request):
    if request.method=="GET":
        return render(request,'register.html')
    elif request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phoneno=request.POST.get('phoneno')
        password=request.POST.get('password')
        epassword=make_password(password)

        cusobj=customer(name=name,email=email,phoneno=phoneno,password=epassword)
        cusobj.save()
        return redirect('../login/')
    
    
def login(request):
    if request.method=="GET":
        return render(request,'login.html')
    elif request.method =="POST":
        email = request.POST.get('email')
        print(email)
        password = request.POST.get('password')
        print(password)

        cust = customer.objects.filter(email=email)
        if cust:
            custobj = customer.objects.get(email=email)

            flag = check_password(password,custobj.password)

            if True:
                request.session['sessionvalue']=  custobj.email
                travobj=travel_agency.objects.all()
                print(travobj)
                return render(request,'index.html',{"travobj":travobj})
            else:
                return render(request,'login.html',{'msg':'Incorrect username and Password'})
            
        else:
            return render(request,'login.html',{'msg':'Incorrect username and Password'})
        

def travelregister(request):
    if request.method=="GET":
        return render(request,'travelregister.html')
    elif request.method == "POST":
        name = request.POST.get('name')
        # Continue with the rest of your code
        image=request.FILES.get('image')
        email=request.POST.get('email')
        phoneno=request.POST.get('phoneno')
        password=request.POST.get('password')
        description=request.POST.get('description')
        epassword=make_password(password)

        travlogobj=travel_agency(image=image,name=name,email=email,phoneno=phoneno,password=epassword,description=description)
        travlogobj.save()
        return redirect('../travellogin/')
    
def travellogin(request):
    if request.method=="GET":
        return render(request,'travellogin.html')
    if request.method =="POST":
        email = request.POST.get('email')
        print(email)
        password = request.POST.get('password')
        print(password)

        travlog = travel_agency.objects.filter(email=email)
        if travlog:
            travlogobj = travel_agency.objects.get(email=email)
            print(travlogobj)
            flag = check_password(password,travlogobj.password)
            print(flag)

    
            if True:
                request.session['sessionvaluetravel_agency']=  travlogobj.email
                return redirect('../profile/')
            else:
                return render(request,'travellogin.html',{'msg':'Incorrect username and Password'})
            
        else:
            return render(request,'travellogin.html',{'msg':'Incorrect username and Password'})
        


def travel_agencynavbar(request):
    return render(request,'travelnavbar.html')

def travel_agencyprofile(request):
    travel_agencysess = request.session['sessionvaluetravel_agency']
    travlog = travel_agency.objects.filter(email=travel_agencysess)

    travlogobj = None  # Initialize the variable with a default value
    if travlog:
        travlogobj = travel_agency.objects.get(email=travel_agencysess)

    return render(request, 'profile.html', {'session': travel_agencysess, 'travlogobj': travlogobj})

def traveleditprofile(request):
    if request.method == 'GET':
        return render(request,'traveleditprofile.html')
    if request.method == 'POST':
        image=request.FILES.get('image')
        name = request.POST.get('name')
        # image=request.FILES.get('image')
        email=request.POST.get('email')
        phoneno=request.POST.get('phoneno')
        description=request.POST.get('description')
            
        travel_agencysess=request.session['sessionvaluetravel_agency']
        travlog=travel_agency.objects.filter(email=travel_agencysess).update(image=image,name=name,email=email,phoneno=phoneno,description=description)
        return redirect('../profile/')
    
def addpackage(request):

    if request.method == 'POST':
       
        iid=request.POST.get('iid')
        travel_agencysess=request.session['sessionvaluetravel_agency']
        travlogobj=travel_agency.objects.get(email=travel_agencysess)

        image=request.FILES.get('image')
        package_name = request.POST.get('package_name')
        package_description = request.POST.get('package_description')
        # name=request.POST.get('name')
        package_price= request.POST.get('package_price')
        video=request.FILES.get('video')
       
        
        new_package = package(
            image=image,
            package_name=package_name,
            package_description=package_description,
            # name=name,
            package_price=package_price,
            video=video,
            travel_agencyid=travlogobj
        )
        new_package.save()

        return redirect('../viewpacakge/')  



    return render(request, 'addpackage.html')



def viewpacakge(request):
    travel_agencysess=request.session['sessionvaluetravel_agency']
    
    travlog=travel_agency.objects.filter(email=travel_agencysess)
    if travlog:

        travlogobj=travel_agency.objects.get(email=travel_agencysess)
        cobj=package.objects.filter(travel_agencyid=travlogobj.id)
       

        return render(request,'viewpacakge.html',{'cobj':cobj})

 
class deletepackege(DeleteView):
    model = package
    template_name='deletetask.html'
    success_url=reverse_lazy('viewpackage')

class detailpackage(DetailView):
    model =package
    template_name = 'packagedetail.html'
    context_object_name='i'


def editpacakge(request, pk):
    package_obj = get_object_or_404(package, id=pk)

    if request.method == 'POST':
        package_obj.package_name = request.POST.get('package_name')
        package_obj.package_description = request.POST.get('description')
        package_obj.package_price = request.POST.get('package_price')
        

        
        if 'image' in request.FILES:
            package_obj.image = request.FILES['image']

        
        package_obj.save()

        return redirect('../viewpacakge/', package_id=package_obj.id)
    
    context = {
        'package': package,
        'cobj': package_obj
    }


    return render(request, 'editpacakge.html', context)


def travel_agencylogout(request):
    del(request.session['sessionvaluetravel_agency'])
    return redirect('../travellogin')   

def addtocart(request):
    packageid = request.POST.get('packageid')
    cussession = request.session['sessionvalue']  # email of customer
    cusobj = customer.objects.get(email=cussession)  # fetch repacakgelid from database table using email
    pacobj = package.objects.get(id=packageid)

    # Check if the package is already in the cart
    flag = cart.objects.filter(custid=cusobj.id, pacakgelid=pacobj.id).exists()
    if not flag:
        # Add package to cart if it is not already there
        cartobj = cart(custid=cusobj, pacakgelid=pacobj, quantity=1, totalamount=pacobj.package_price)
        cartobj.save()

    return redirect('../packageview/')

def viewcart(request):
    cussession = request.session['sessionvalue'] #email of customer
    cusobj = customer.objects.get(email = cussession) 
    cartobj = cart.objects.filter(custid = cusobj.id)

    return render(request,'viewcart.html',{'cartobj':cartobj,'session':cussession })

def removepacakge(request):
    packageid = request.POST.get('packageid')
    cussession = request.session['sessionvalue']  # email of customer
    cusobj = customer.objects.get(email=cussession)  # fetch repacakgelid from database table using email
    custid = cusobj.id  # fetch customer id using customer object
    pacobj = package.objects.get(id=packageid)

    flag = cart.objects.filter(custid=cusobj.id, pacakgelid=pacobj.id)
    if flag:
        cartobj = cart.objects.get(custid=cusobj.id, pacakgelid=pacobj.id)
        if cartobj.quantity > 1:
            cartobj.quantity -= 1
            cartobj.totalamount = pacobj.package_price * cartobj.quantity
            cartobj.save()
        else:
            cartobj.delete()

    return redirect('../viewcart/')
   


def summary(request):
    cussession=request.session['sessionvalue']
    cusobj=customer.objects.get(email=cussession)
    cartobj=cart.objects.filter(custid=cusobj.id)
    totalbill=0
    for i in cartobj:
        totalbill=i.totalamount+totalbill
    return render(request,'summary.html',{'session':cussession,'cartobj':cartobj,'totalbill':totalbill})

def placeorder(request):
    fn=request.POST.get('fn')
    ln=request.POST.get('ln')
    phoneno=request.POST.get('phoneno')
    address=request.POST.get('address')
    city=request.POST.get('city')
    state=request.POST.get('state')
    pincode=request.POST.get('pincode')
   

    datev=date.today()
    print(datev)
    orderobj=order(firstname=fn,lastname=ln,phoneno=phoneno,address=address,city=city,state=state,pincode=pincode,orderstatus='pending',orderdate=datev)
    orderobj.save()
    

    ono=str(orderobj.id)+str(datev).replace('-','')
    orderobj.ordernumber=ono
    orderobj.save()

    cussession=request.session['sessionvalue']
    cusobj=customer.objects.get(email=cussession)
    cartobj=cart.objects.filter(custid=cusobj.id)

    totalbill = 0 
    for i in cartobj:
        totalbill=i.totalamount+totalbill

    sm=EmailMessage('order placed','order placed frompet store application.Total bill for your order is'+str(totalbill),to=['sakpalpurva4@gmail.com'])
    sm.send()
    return render(request,'payment.html',{'orderobj':orderobj,'session':cussession,'cartobj':cartobj,'totalbill':totalbill})

def order_detail(request):
    cussession = request.session['sessionvalue']
    cusobj = customer.objects.get(email=cussession)
    orders = order.objects.filter(firstname=cusobj.name)

    return render(request, 'orderdetail.html', {'session': cussession, 'orders': orders})


def success(request):
    orderid = request.GET.get('order_id')
    tid = request.GET.get('payment_id')
    request.session['sessionvalue'] = request.GET.get('session')
    cussession=request.session['sessionvalue']
    cusobj=customer.objects.get(email=cussession)
    cartobj=cart.objects.filter(custid=cusobj.id)
    orderobj=order.objects.get(ordernumber = orderid)

    paymentobj=payment(customerid=cusobj,oid=orderobj,paymentstatus="Paid",transactionid=tid)
    paymentobj.save()

    for i in cartobj:
        orderdetailobj=orderdetail(paymentid=paymentobj,ordernumber=orderid,packagetid=i.pacakgelid,customerid=i.custid,quantity=i.quantity,totalprice=i.totalamount)
        orderdetailobj.save()
        i.delete()

    totalbill = 0
    for i in cartobj:
        totalbill = i.totalamount + totalbill

    return render(request,'success.html',{'session':cussession,'payobj':paymentobj, 'order':orderobj, 'cartobj': cartobj,  'totalbill' :totalbill})



def my_order(request):
    cussession = request.session['sessionvalue']
    cusobj = customer.objects.get(email=cussession)
    my_order = orderdetail.objects.filter(customerid=cusobj.id)

    return render(request, 'my_order.html', {'session': cussession, 'my_order': my_order})

def logout(request):
    del(request.session['sessionvalue'])
    return redirect('../login/')







