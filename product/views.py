from django.shortcuts import render, redirect
from django.contrib import messages
from product.models import Product, Category
from Bidding.models import Bid, WatchList, Deposite
from Content.models import Ads

from product.serializers import ProductSerializer, CategorySerializer
from rest_framework.generics import ListAPIView

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils import timezone  # Import the timezone module

from django.http import Http404



class ProductDetail(APIView):
    def get_object(self, category_id, product_id):
        try:
            return Product.objects.filter(category__id=category_id).get(id=product_id)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, category_id, product_id, format=None):
        product = self.get_object(category_id, product_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class Notices(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(start_date_offset_in_minutes__gt=0).order_by('-datetime')[:8]


class LatestProductsList(ListAPIView):
    queryset = Product.objects.all().order_by('-datetime')[:8]
    serializer_class = ProductSerializer


class AllCategories(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class AddProduct(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            image = request.FILES.get("thumbNails")
            serializer.save(user=request.user, thumbNails=image, datetime=timezone.now())
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def home(request):
    products = Product.objects.all().order_by('category','-datetime')
    ads = Ads.objects.all()
    carousel = Product.objects.all().order_by('-datetime')
    category = Category.objects.all()
    # /print(products)
    content = {'ads': ads, 'products': products, 'category': category, 'carousel': carousel}
    return render(request, 'index.html', content)


def category(request, id):
    products = Product.objects.filter(category=Category.objects.get(id=id)).order_by('datetime')
    category = Category.objects.get(id=id)
    return render(request, 'Category.html', {'products': products, 'category': category})
# def product_view(request):
#
#     return render(request, 'index.html', {'products': products})


def bid_so_far(request, id):
    bid = Bid.objects.filter(product__id=id).order_by('-datetime__time')
    return render(request, 'BidSofar.html', {'bid': bid})


def product_detail(request, id):
    product = Product.objects.get(id=id)
    bid = Bid.objects.filter(product__id=id).order_by('-datetime')
    try:
        deposite = Deposite.objects.get(user=request.user)
    except:
        deposite = None
    watchlist = WatchList.objects.filter(product=product)
    b = bid.first()
    ctime = product.remaining_time_in_minutes()
    context = { 'watch':watchlist, 'product': product, 'ctime': ctime, 'bid': bid, 'b': b}
    return render(request, 'Product.html', context )


def sell(request):
    category = Category.objects.all()
    if request.method == 'POST':
        title = request.POST["title"]
        categ = request.POST["Category"]
        price = request.POST["price"]
        description = request.POST['desc']
        thumbnails = request.FILES['thumb']
        images = request.FILES['Image']

        counter = int(request.POST['duration'])

        product = Product(title=title, category=Category.objects.get(id=categ), user=request.user
                          , price=price, description=description, thumbNails=thumbnails
                          ,images=images, duration_in_minutes=counter*60,
                          state=Product.STATE.RUNNING)
        product.save()
        messages.success(request, 'Product added to Auction')
        return redirect('Home')
#
    return render(request, 'Sell.html', {'category': category})
