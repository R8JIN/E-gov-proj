from django.urls import path
from Bidding.views import add_to_watchlist, add_bid, watchlist, cart, add_cart

urlpatterns = [
    path('add_watchlist/<id>', add_to_watchlist, name='watchlist'),
    path('bid/<id>', add_bid, name='bid'),
    path('watchlist', watchlist, name='watch'),
    path('cart', cart, name='cart'),
    path('add_cart', add_cart, name='add_cart')
]