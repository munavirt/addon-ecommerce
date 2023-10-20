from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from .models import Category,Product
from django.db.models import Q
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
# Create your views here.
def home(request):
    products = Product.objects.all().filter(is_available=True)
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories
    }
    return render(request,'index.html',context)


def store(request,store_slug=None):
    category = None
    products = None

    if store_slug != None:
        categories = get_object_or_404(Category,slug=store_slug)
        products = Product.objects.filter(category=categories,is_available=True)
        paginator = Paginator(products,12)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        paginator = Paginator(products,6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    context = {
        'products': paged_products,
        'product_count' : product_count
    }
    return render(request,'category.html',context)


def product_details(request,store_slug,product_slug):
    try:
        single_product = Product.objects.get(category__slug=store_slug, slug=product_slug)
    except Exception as e:
        raise

    context = {
        'single_product' : single_product
    }
    return render(request,'product_details.html',context)

def search(request):
    products = []  # Initialize products with an empty list

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    else:
        product_count = 0

    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/category.html', context)


def contact_us(request):
    return render(request,'contact.html')


def send_whatsapp_message(request, product_id):
    try:
        single_product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        # Handle the case where the product doesn't exist.
        return HttpResponse("Product not found")

    # Create a WhatsApp message URL with the product details
    message = f"Check out this product: {single_product.product_name}, Price: ${single_product.new_price}. Description: {single_product.description}"
    whatsapp_url = f"https://wa.me/+916238142442/?text={message}"

    # Redirect the user to WhatsApp
    return redirect(whatsapp_url)

