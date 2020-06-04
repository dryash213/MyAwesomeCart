from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,Contact,Orders,OrderUpdate
from math import ceil
import json
# Create your views here.



def index(request):
    # all_objects = Product.objects.all()
    # # print(all_objects)
    # for item in all_objects:
    #     print(item.product_name)
    #     params = {'all_items': all_objects}
    # products=Product.objects.all()
    # print(products)
    # n=len(products)
    # nSlides =n//4 +ceil((n/4)-(n//4))
    #params={'no_of_slides':nSlides, 'range':range(1,nSlides),'product':products}
    # allProds=[[products,range(1,nSlides),nSlides],
    #           [products,range(1,nSlides),nSlides]]
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params={'allProds':allProds}
    return render(request, 'shop/index.html',params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method=="POST":
        # print(request)
        name=request.POST.get('name','')
        phone=request.POST.get('phone','')
        email=request.POST.get('email','')
        desc=request.POST.get('desc','')

        print(name,email,phone,desc)
        contact=Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()

    return render(request, 'shop/contact.html')


def tracker(request):
    if request.method=="POST":
        orderId=request.POST.get('orderId','')
        email=request.POST.get('email','')
        try:
            order=Orders.objects.filter(order_id=orderId,email=email)
            if len(order)>0:
                update=OrderUpdate.objects.filter(order_id=orderId)
                updates=[]
                for item in update:
                    updates.append({'text':item.update_desc,'time':item.timestamp})
                    response=json.dumps([updates,order[0].items_json],default=str)
                    return HttpResponse(response)
            else:
                    return HttpResponse({})
        except Exception as e:
                return HttpResponse({})
            

    return render(request, 'shop/tracker.html')


def search(request):
    return render(request, 'shop/search.html')


def productview(request,myid):
    product = Product.objects.filter(id=myid)
    print(product)
    return render(request, 'shop/productview.html',{'product':product[0]})


def checkout(request):
    if request.method=="POST":
        # print(request)
        name=request.POST.get('name','')
        items_json=request.POST.get('itemsJson','')
        city=request.POST.get('city','')
        email=request.POST.get('email','')
        zip_code=request.POST.get('zip_code','')
        state=request.POST.get('state','')
        phone=request.POST.get('phone','')
        address=request.POST.get('address1','')+" "+request.POST.get('address2','')
        order=Orders(items_json=items_json,name=name,email=email,address=address,city=city,zip_code=zip_code,state=state,phone=phone)
        order.save()
        update=OrderUpdate(order_id=order.order_id,update_desc="The order have been placed successfully")
        update.save()
        thank=True
        id=order.order_id
        return render(request,'shop/checkout.html',{'thank':thank,'id':id})
    #Fectch the product using the Id
    return render(request, 'shop/checkout.html')
