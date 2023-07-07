from django.urls import path
from Bidding.views import add_to_watchlist, add_bid, watchlist, cart, add_cart, execute_payment, create_payment, remove_from_watchlist

urlpatterns = [
    path('add_watchlist/<id>', add_to_watchlist, name='watchlist'),
    path('remove_from_watchlist/<id>', remove_from_watchlist, name='remove'),
    path('bid/<id>', add_bid, name='bid'),
    path('watchlist', watchlist, name='watch'),
    path('cart', cart, name='cart'),
    path('add_cart', add_cart, name='add_cart'),
    path('payment/create/<id>', create_payment, name='payment'),
    path('payment/execute/', execute_payment, name='execute'),
]