from django.urls import path
from product.views import home, product_detail, bid_so_far, sell, category, LatestProductsList, AllCategories, AddProduct, Notices, ProductDetail
urlpatterns = [
    path('', home, name='Home'),
    # path('product', product_view),
    path('product/<id>', product_detail, name='Prod_view'),
    path('bid_so_far/<id>', bid_so_far, name='bidsofar'),
    path('sell/', sell, name='sell'),
    path('category/<id>', category, name='category'),
    path('latest-products/', LatestProductsList.as_view(), name='latest-post'),
    path('all-categories/', AllCategories.as_view(), name='all-categories'),
    path('add-product/', AddProduct.as_view(), name='add-product'),
    path('notices/', Notices.as_view(), name='notices'),
    path('category/<int:category_id>/<int:product_id>/', ProductDetail.as_view(), name='product-detail'),

]