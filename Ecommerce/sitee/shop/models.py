from django.db import models

# Create your models here.
class Product(models.Model):
    product_id= models.AutoField
    product_name=models.CharField(max_length=60)
    desc=models.CharField(max_length=400)
    category = models.CharField(max_length=60,default="")
    subcategory = models.CharField(max_length=60,default="")
    price = models.IntegerField(default=0)
    image=models.ImageField(upload_to='shop/images',default="")
    pub_date= models.DateField()

    def __str__(self):
        return self.product_name

class Contact(models.Model):
    msg_i2d= models.AutoField
    name=models.CharField(max_length=60)
    desc=models.CharField(max_length=400,default="")
    phone = models.CharField(max_length=15,default="")
    email = models.CharField(max_length=50,default="")
    
    def __str__(self):
        return self.name

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=111)
    address = models.CharField(max_length=400)
    city = models.CharField(max_length=111)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=12, default="")    

class OrderUpdate(models.Model):
    update_id  = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."        
          
