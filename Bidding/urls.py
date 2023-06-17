from django.urls import path
from Bidding.views import add_to_watchlist, add_bid, watchlist, cart, add_cart, create_payment, execute_payment
urlpatterns = [
    path('add_watchlist/<id>', add_to_watchlist, name='watchlist'),
    path('bid/<id>', add_bid, name='bid'),
    path('watchlist', watchlist, name='watch'),
    path('cart', cart, name='cart'),
    path('add_cart', add_cart, name='add_cart'),
    path('payment/create/<id>', create_payment, name='payment'),
    path('payment/execute/', execute_payment, name='execute_payment')
    # path('cancel-payment/', cancel_payment, name='cancel_payment'),

]