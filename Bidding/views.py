import paypalrestsdk
from django.shortcuts import render, redirect, HttpResponse
from product.models import Product
from .models import WatchList, Bid, Cart, Order
from django.contrib import messages
from paypalrestsdk import Payment
# Create your views here.
from django.conf import settings

def create_payment(request, id):
    paypalrestsdk.configure(
        mode=settings.PAYPAL_MODE,
        client_id=settings.PAYPAL_CLIENT_ID,
        client_secret=settings.PAYPAL_CLIENT_SECRET
    )

    product = Product.objects.get(id=id)
    order = Order.objects.filter(product__id=id)
    if not order:
        order = Order(user=request.user, product=product, address=request.user.address,
                      mobile=request.user.mobile, price=product.final_price)
        # order.save()
    # Get the amount and recipient email from the form or request data  # Assuming you have a form field for the recipient's email

        payment = Payment({
            'intent': 'sale',
            'payer': {
                'payment_method': 'paypal'
            },
            'redirect_urls': {
                'return_url': 'http://127.0.0.1:8000/biddingpayment/execute/',
                'cancel_url': 'http://localhost:8000/payment/cancel/'
            },
            'transactions': [{
                'amount': {
                    'total': product.final_price,
                    'currency': 'USD'
                },
                'payee': {
                    'email': 'rojin1234@gmail.com'
                }
            }]
        })

        if payment.create():
            for link in payment.links:
                if link.rel == 'approval_url':
                    redirect_url = link.href
                    order.save()
                    return redirect(redirect_url)
        else:
            return render(request, 'payment_failed.html')
    else:
        messages.warning(request,"You've already order")
        return redirect('/')


def execute_payment(request):
    payer_id = request.GET.get('PayerID')
    payment_id = request.GET.get('paymentId')


    paypalrestsdk.configure(
        mode=settings.PAYPAL_MODE,
        client_id=settings.PAYPAL_CLIENT_ID,
        client_secret=settings.PAYPAL_CLIENT_SECRET
    )
    payment = Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return render(request, 'payment_success.html', {})
    else:
        return HttpResponse("Payment failed")


def watchlist(request):
    product = WatchList.objects.filter(user=request.user).order_by('-datetime')
    return render(request, 'WatchList.html', {'product': product})


def add_to_watchlist(request, id):
    product = WatchList.objects.filter(user=request.user).filter(id=id)
    if not product:
        product = WatchList(user=request.user, product=Product.objects.get(id=id))
        product.save()
        messages.success(request, 'Added to your watchlist')
    else:
        messages.warning(request, 'Already exist in your watchlist')

    return redirect('Home')


def remove_from_watchlist(request, id):
    product = WatchList.objects.get(id=id)

    product.delete()
    messages.warning(request, 'Removed from the watchlist')
    return redirect('watchlist')

def add_bid(request, id):
    product = Product.objects.get(id=id)
    if request.user == product.user:
        messages.warning(request, 'You are the auctioneer')
        return redirect('/')
    else:
        if request.method == 'POST':
            amount = request.POST['amt']
            b = Bid.objects.filter(product__id=id)
            if not b:
                if float(amount) < float(product.price):
                    messages.error(request, f'Bid amount should be more than {product.price}')
                    return redirect('/')
            else:
                if float(amount) < b.last().bid_amt:
                    messages.error(request, f'Bid amount should be more than bid amount Rs. {b.last().amount}')
                    return redirect('/')
            bid = Bid(user=request.user, product=Product.objects.get(id=id), bid_amt=amount)
            bid.save()
            messages.success(request, 'Bid submitted')
        return redirect('Home')


def cart(request):
    add_cart()
    product = Cart.objects.filter(user=request.user)
    return render(request, 'Cart.html', {'product': product})



def add_cart():
    products = Product.objects.all()

    for p in products:
        ctime = p.remaining_time_in_minutes()
        if ctime == 0:
            bid = Bid.objects.filter(product__id=p.id)
            # print(bid)
            if bid:
                bid = bid.last()
                p.final_price = bid.bid_amt;
                p.save()
                print(bid.product.id)
                cart = Cart.objects.filter(user=bid.user).filter(product__id=bid.product.id)
                if not cart:
                    cart = Cart(user=bid.user, product=Product.objects.get(id=bid.product.id))
                    cart.save()





