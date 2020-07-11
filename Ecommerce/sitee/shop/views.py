from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,Contact,Orders,OrderUpdate
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from PayTm import checksum
MERCHANT_KEY = 'kbzk1DSbJiV_O3p5';



# Get an instance of a logger
# logger = logging.getLogger(__name__)
# Create your views here.
from django.http import HttpResponse


# # Create your views here.
def index (request):
    allprods =[]
    catprods = Product.objects.values('category','id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n= len(prod)
        nSlide= n//4 + ceil((n//4)-(n//4 ))        
        allprods.append([prod,range(1, nSlide),nSlide ])
    prashant={'allprods':allprods}
    return render(request,'shop/index.html',prashant)
def searchMatch(query,item):
    ''' return true only if query matches item '''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:    
        return False    
def search(request):
    query= request.GET.get('search')
    allprods =[]
    catprods = Product.objects.values('category','id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod= [item for item in prodtemp if searchMatch(query,item)]
        n= len(prod)
        nSlide= n//4 + ceil((n//4)-(n//4 ))
        if len(prod) != 0:
            allprods.append([prod,range(1, nSlide),nSlide ])
    prashant={'allprods':allprods,"msg":""}
    if len(allprods) == 0 or len(query)<4:
        prashant={'msg':"Please make sure to enter revelent query "}
    return render(request,'shop/search.html',prashant)
def about(request):
    return render(request,'shop/about.html')
def contact(request):
    thank=False
    if request.method=="POST":
        name= request.POST.get('name', '')
        email= request.POST.get('email', '')
        phone=request.POST.get('phone', '')
        desc= request.POST.get('desc', '')
        contact=Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
        thank= True
    return render(request,'shop/contact.html',{'thank':thank})
def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success","updates":updates,"itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')
    return render(request,'shop/tracker.html')

def productview(request,myid):
    # fetch the product through id
    product = Product.objects.filter(id=myid)
    # print(pro duct)
    return render(request,'shop/prodview.html',{'product': product[0]})
def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city, state=state, zip_code=zip_code, phone=phone,amount=amount)
        order.save()
        update= OrderUpdate(order_id=order.order_id,update_desc= "The order has been placed")
        order.save()
        thank = True
        id = order.order_id
        
        return render(request,'shop/checkout.html', {'thank':thank, 'id': id})

        # request patm to tranfer the amount after payment by user
    #     param_dict = {
            
    #         'MID':'WorldP64425807474247',
    #         'ORDER_ID':str(order.order_id),
    #         'TXN_AMOUNT':str(amount),
    #         'CUST_ID':'email',
    #         'INDUSTRY_TYPE_ID':'Retail',
    #         'WEBSITE':'WEBSTAGING',
    #         'CHANNEL_ID':'WEB',
	#         'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',        
    #     }
    #     param_dict['CHECKSUMHASH'] = checksum.generate_checksum(param_dict,MERCHANT_KEY)
    #     return render(request,'shop/paytm.html',{'param_dict':param_dict})
    return render(request,'shop/checkout.html')
  
@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here 
    form = request.POST
    response_dict ={}
    for i in form.keys():
        response_dict[i]=form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    varify= checksum.varify_checksun(response_dict,MERCHANT_KEY,checksum)
    if varify:
        if response_dict['RESPCODE']=='01':
            print('order successful')
    else:
        print('order was not successful because'+response_dict['RESPMSG'])



    return render(respect,'shop/paymentstatus.html',{'response':response_dict})