from django.db import models

class customer(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField()
    phoneno=models.BigIntegerField()
    password=models.CharField(max_length=200)

    class Meta:
        db_table="customer"

class travel_agency(models.Model):
    
    image=models.ImageField(upload_to='media',null=True, blank=True)
    name =models.CharField(max_length=200)
    email=models.EmailField()
    phoneno=models.BigIntegerField()
    password=models.CharField(max_length=500)
    description=models.CharField(max_length=500,null=True)
    class Meta:
        db_table="travel_agency"

class package(models.Model):
    image=models.ImageField(upload_to='media',null=True)
    package_name=models.CharField(max_length=100,null=True)
    travel_agencyid=models.ForeignKey(travel_agency,on_delete=models.CASCADE)
    package_price=models.FloatField(null=True)
    package_description=models.CharField(max_length=500,null=True)
    video = models.FileField(upload_to='videos/')
    status_choice=(
        ("APPROVED","APPROVED"),
        ("UNAPPROVED","UNAPPROVED")
    )
    status=models.CharField(max_length=100,choices=status_choice,default="pending")

    class Meta:
        db_table="travel"

class cart(models.Model):
    custid = models.ForeignKey(customer,on_delete=models.CASCADE)
    pacakgelid = models.ForeignKey(travel_agency,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    totalamount= models.FloatField()

    class Meta:
        db_table='cart'

class order(models.Model):
    ordernumber=models.CharField(max_length=200)
    orderdate=models.DateField()
    firstname=models.CharField(max_length=200)
    lastname=models.CharField(max_length=200)
    phoneno=models.BigIntegerField()
    address=models.CharField(max_length=200)
    city=models.CharField(max_length=200)
    state=models.CharField(max_length=200)
    pincode=models.IntegerField()
    orderstatus=models.CharField(max_length=200)

    class Meta:
        db_table='order'

class payment(models.Model):
    customerid=models.ForeignKey(customer,on_delete=models.CASCADE)
    oid=models.ForeignKey(order,on_delete=models.CASCADE)
    paymentstatus=models.CharField(max_length=200,default="pending")
    transactionid=models.CharField(max_length=200)
    paymentmode=models.CharField(max_length=100,default="paypal")

    class Meta:
        db_table="payment"

class orderdetail(models.Model):
    ordernumber=models.CharField(max_length=100)
    customerid=models.ForeignKey(customer,on_delete=models.CASCADE)
    packageid=models.ForeignKey(package,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    totalprice=models.IntegerField()
    paymentid=models.ForeignKey(payment,on_delete=models.CASCADE,null=True)
    created_at=models.DateField(auto_now=True)
    updated_at=models.DateField(auto_now=True)

    class Meta:
        db_table='orderdetail'
        

# Create your models here.
