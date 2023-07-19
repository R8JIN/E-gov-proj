from django.shortcuts import render, redirect, HttpResponse
from product.models import Product
from .models import WatchList, Bid, Cart, Order, Deposite
from django.contrib import messages
import paypalrestsdk
from django.conf import settings
from paypalrestsdk import Payment
from django.contrib.auth.decorators import login_required
from Account.models import User

def create_payment(request, id):
    paypalrestsdk.configure(
        mode=settings.PAYPAL_MODE,
        client_id=settings.PAYPAL_CLIENT_ID,
        client_secret=settings.PAYPAL_CLIENT_SECRET
    )

    product = Product.objects.get(id=id)
    deposite = Deposite.objects.get(user=request.user, product=product)
    print(product)
    your_pay = product.final_price - deposite.depo_amt
    payment = Payment({
        'intent': 'sale',
        'payer': {
            'payment_method': 'paypal'
        },
        'redirect_urls': {
            'return_url': 'http://localhost:8000/biddingpayment/execute/%s/%s' %(request.user.id, id),
            'cancel_url': 'http://localhost:8000/payment/cancel/'
        },
        'transactions': [{
            'amount': {
                'total': your_pay,
                'currency': 'USD'
            },
            'payee': {
                'email': 'rojin1234@gmail.com'
            },
            "description": f"This is the payment transaction for  ."}
        ]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == 'approval_url':
                redirect_url = link.href
                return redirect(redirect_url)
    else:
        return render(request, 'payment_failed.html')


def execute_payment(request, uid, id):
    print(request.user)
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    paypalrestsdk.configure(
        mode=settings.PAYPAL_MODE,
        client_id=settings.PAYPAL_CLIENT_ID,
        client_secret=settings.PAYPAL_CLIENT_SECRET
    )
    payment = Payment.find(payment_id)
    if payment.execute({'payer_id': payer_id}):
        p = Product.objects.get(id=id)
        # Payment executed successfully

        order = Order(user=User.objects.get(id=uid), product=Product.objects.get(id=id),
                      price=p.final_price)
        cart_ob = Cart.objects.get(product=Product.objects.get(id=id))
        cart_ob.status = 'Paid'
        cart_ob.save()
        order.save()
        messages.success(request, "Payment Done")
        return redirect('invoice', id=p.id)
    else:
        return HttpResponse('Payment execution failed.')




def watchlist(request):
    products = WatchList.objects.filter(user=request.user).order_by('-datetime')
    # print(products)
    return render(request, 'WatchList.html', {'products': products})


def view_invoice(request, id):
    order = Order.objects.get(product=Product.objects.get(id=id))
    return render(request, 'ProductInvoice.html', {'order': order})

def add_to_watchlist(request, id):
    product = WatchList.objects.filter(user=request.user).filter(product_id=id)
    if not product:
        product = WatchList(product=Product.objects.get(id=id), user=request.user)
        product.save()
        messages.success(request, 'Added to your watchlist')
    else:
        messages.warning(request, 'Already exist in your watchlist')
    return redirect('Home')


def remove_from_watchlist(request, id):
    product = WatchList.objects.filter(user=request.user).filter(id=id)
    product.delete()
    messages.success(request, 'Removed from the watchlist')
    return redirect('Home')


def add_bid(request, id):
    product = Product.objects.get(id=id)
    user_bid = Bid.objects.filter(user=request.user, product=product)
    try:
        depo = Deposite.objects.get(user=request.user, product=product)
    except:
        depo = None

    if request.user == product.user:
        messages.warning(request, 'You are the auctioneer')
        return redirect('http://localhost:8000/product/%s' % id)
    else:
        if(depo):
            if(not user_bid):
                if request.method == 'POST':
                    amount = request.POST['amt']
                    b = Bid.objects.filter(product__id=id).order_by('bid_amt')

                    if float(amount) < float(product.price)+10/100*float(product.price):
                        messages.error(request, f'Bid amount should be more than {product.price}')
                        return redirect('http://localhost:8000/product/%s' % id)
                    """English Auction ko logic hai"""
                    # if not b:
                    #     if float(amount) < float(product.price)+10/100*float(product.price):
                    #         messages.error(request, f'Bid amount should be more than {product.price}')
                    #         return redirect('http://localhost:8000/product/%s' % id)
                    # else:
                    #     if float(amount) < b.last().bid_amt + 10/100*float(b.last().bid_amt):
                    #         messages.error(request, f'Bid amount should be more than bid amount Rs. {b.last().bid_amt}')
                    #         return redirect('http://localhost:8000/product/%s' % id)
                    bid = Bid(user=request.user, product=Product.objects.get(id=id), bid_amt=amount)
                    bid.save()
                    messages.success(request, 'Bid submitted')
            else:
                messages.warning(request, "You have already submitted your bid")
        else:
            messages.error(request, "You need to deposite")
            return render(request, 'deposite.html', {'product':product, 'depo': product.price*0.1})
    return redirect('Home')


def cart(request):
    add_cart()
    product = Cart.objects.filter(user=request.user)
    order = Order.objects.filter(user=request.user)
    print(product)
    return render(request, 'Cart.html', {'product': product, 'order': order})



def add_cart():
    products = Product.objects.all()
    for p in products:
        ctime = p.remaining_time_in_minutes()
        if ctime == 0:
            bid = Bid.objects.filter(product__id=p.id).order_by('bid_amt')
            if bid:
                bid = bid.last()
                b = Bid.objects.filter(product__id=p.id, bid_amt=bid.bid_amt)
                if b.count() > 1:
                    bid_price = b.order_by("datetime");
                    bid = bid_price.first()
                p.final_price = bid.bid_amt;
                p.save()
                print(bid.product.id)
                cart = Cart.objects.filter(user=bid.user).filter(product__id=bid.product.id)
                if not cart:
                    cart = Cart(user=bid.user, product=Product.objects.get(id=bid.product.id))
                    cart.save()



#deposite ko lagi
def create_deposite(request, id):
    paypalrestsdk.configure(
        mode=settings.PAYPAL_MODE,
        client_id=settings.PAYPAL_CLIENT_ID,
        client_secret=settings.PAYPAL_CLIENT_SECRET
    )

    product = Product.objects.get(id=id)

    print(product)
    payment = Payment({
        'intent': 'sale',
        'payer': {
            'payment_method': 'paypal'
        },
        'redirect_urls': {
            'return_url': 'http://localhost:8000/biddingdeposite/execute/%s'% id,
            'cancel_url': 'http://localhost:8000/payment/cancel/'
        },
        'transactions': [{
            'amount': {
                'total': product.price*10/100,
                'currency': 'USD'
            },
            'payee': {
                'email': 'rojin1234@gmail.com'
            },
            "description": f"This is the payment transaction for  ."}
        ]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == 'approval_url':
                redirect_url = link.href
                return redirect(redirect_url)
    else:
        return render(request, 'payment_failed.html')

#deposite execute 
def execute_deposite(request, id):
    print(request.user)
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    paypalrestsdk.configure(
        mode=settings.PAYPAL_MODE,
        client_id=settings.PAYPAL_CLIENT_ID,
        client_secret=settings.PAYPAL_CLIENT_SECRET
    )
    payment = Payment.find(payment_id)
    if payment.execute({'payer_id': payer_id}):
        p = Product.objects.get(id=id)
        # Payment executed successfully
        print(request.user)
        depo = Deposite(user=request.user, product=Product.objects.get(id=id),
                      depo_amt=p.price*10/100)
        depo.save()
        messages.success(request, "Payment Done")
        return render(request, 'Payment.html', {})
    else:
        return HttpResponse('Payment execution failed.')






