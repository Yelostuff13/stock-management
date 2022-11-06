from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from store.models import Film,Product,Cart,CartItem,Order,OrderItem
from django.core.paginator import Paginator,EmptyPage,InvalidPage


# Create your views here.
def index(request,product_slug=None):
    Films=None
    product_page=None #หมวดหมู่สินค้า
    #2เงื่อนไข ระบุชื่อกับไม่ระบุ
    if product_slug != None: 
        product_page=get_object_or_404(Product,slug=product_slug)
        Films=Film.objects.all().filter(product=product_page,available=True)
    else :
        Films=Film.objects.all().filter(available=True)


    paginator=Paginator(Films,6)
    try:
        page=int(request.GET.get('page','1'))
    except:
        page=1

    try:
        filmperPage=paginator.page(page)
    except (EmptyPage,InvalidPage):
        filmperPage=paginator.page(paginator.num_pages)
    

    return render(request, 'index.html',{'Films':filmperPage,'Product':product_page}) #{define object key and value}

def product(request):
    return render(request, 'product.html')

def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

def addCart(request,film_id):
    #รหัสสินค้า
    #ดึงรหัสสินค้าตามรหัสที่ส่งมา
    film=Film.objects.get(id=film_id)
    #ตรวจเช็คว่าสร้างตะกร้าสินค้าขึ้นมาหรือยัง 
    #เคยมีตะกร้าสินค้าอยู่แล้ว(ลูกค้าเก่าที่ยังไม่ได้ชำระเงินแล้วอยากจะซื้อของเพิ่ม)
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
    #ยังไม่มีตะกร้าสินค้า
    except Cart.DoesNotExist: #เมื่อไม่พบตะกร้าสิค้า(object cart)
        cart=Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    try:
        #ซื้อรายการสินค้าซ้ำ
        cart_item=CartItem.objects.get(film=film,cart=cart)
        if cart_item.quantity<cart_item.film.stock :
            #เปลี่ยนจำนวนรายการสินค้า
            cart_item.quantity+=1
            #บันทึก/อัพเดทค่า
            cart_item.save()
    except CartItem.DoesNotExist: #DoesNotExist:cartitemยังไม่เคยถูกสร้าง/บันทึกลงฐานข้อมูล
        #ซื้อรายการสินค้าครั้งแรก
        #บันทึกลงฐานข้อมูล
        cart_item=CartItem.objects.create(
            film=film, #ชื่อcolumn=สินค้าที่กดเลือกที่หน้าเว็บ
            cart=cart, #ชื่อcolumn=ตะกร้าสินค้าที่สร้างขึ้นมา
            quantity=1 
        )
        cart_item.save()
    return redirect('/')

def cartdetail(request):
    total=0
    counter=0
    cart_items=None
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request)) #ดึงตะกร้า
        cart_items=CartItem.objects.filter(cart=cart,active=True) #ดึงข้อมูลสินค้าในตะกร้า
        for item in cart_items:
            total+=(item.film.price*item.quantity)
            counter+=item.quantity
    except Exception as e :
        pass

    # if request.method=="POST":
    #     try :           
    #         #บันทึกข้อมูลใบสั่งซื้อ
    #         order=Order.objects.create(
    #             total=total,  
    #         )
    #         order.save()

    #         #บันทึกรายการสั่งซื้อ
    #         for item in cart_items :
    #             order_item=OrderItem.objects.create(
    #                 Film=item.film.name,
    #                 quantity=item.quantity,
    #                 price=item.film.price,
    #                 order=order
    #             )
    #             order_item.save()
    #             #ลดจำนวน Stock
    #             film=Film.objects.get(id=item.film.id)
    #             film.stock=int(item.film.stock-order_item.quantity)
    #             film.save()
    #             item.delete()
    #         return redirect('home')

    #     except Exception as e :
    #         return False , e
        

    return render(request,'cartdetail.html',dict(cart_items=cart_items,total=total,counter=counter))

def CheckOut(request):
    total=0
    counter=0
    cart_items=None
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request)) #ดึงตะกร้า
        cart_items=CartItem.objects.filter(cart=cart,active=True) #ดึงข้อมูลสินค้าในตะกร้า
        for item in cart_items:
            total+=(item.film.price*item.quantity)
            counter+=item.quantity
    except Exception as e :
        pass

    if request.method=="POST":
        name = request.POST.get('name')
        address = request.POST.get('address')
        postcode = request.POST.get('postcode')
        cart=Cart.objects.get(cart_id=_cart_id(request)) #ดึงตะกร้า
        cart_items=CartItem.objects.filter(cart=cart,active=True)

        print(name,address,postcode,cart,cart_items)

        try :   
                    
        
                #บันทึกข้อมูลใบสั่งซื้อ
                order=Order.objects.create(
                    name=name,
                    address=address,
                    postcode=postcode,
                    total=total,  
                )
                order.save()
                print(name)
                #บันทึกรายการสั่งซื้อ
                for item in cart_items :
                    order_item=OrderItem.objects.create(
                        Film=item.film.name,
                        quantity=item.quantity,
                        price=item.film.price,
                        order=order
                    )
                    order_item.save()
                    #ลดจำนวน Stock
                    film=Film.objects.get(id=item.film.id)
                    film.stock=int(item.film.stock-order_item.quantity)
                    film.save()
                    item.delete()
                return redirect('thankyou')
                
        except Exception as e :
                return False , e
            
       
    return HttpResponse("this is checkout page")

def removeCart(request,film_id):
    #ทำงานกับตะกร้าสินค้า A
    cart=Cart.objects.get(cart_id=_cart_id(request))
    #ทำงานกับสินค้าที่จะลบ 1
    film=get_object_or_404(Film,id=film_id)
    cartItem=CartItem.objects.get(film=film,cart=cart)
    #ลบรายการสินค้า 1 ออกจากตะกร้า A โดยลบจาก รายการสินค้าในตะกร้า (CartItem)
    cartItem.delete()
    return redirect('cartdetail')

def search(request):
    #เก็บค่าจากrequest titile->ค้นหาในโมเดลFilm
    Films=Film.objects.filter(name__contains=request.GET['title'])
    return render(request,'index.html',{'Films':Films})

def thankyou(request):
    return render(request,'thankyou.html')
