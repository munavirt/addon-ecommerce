from django.http import JsonResponse
from django.shortcuts import render,redirect
from store.models import Category,Product
from django.db.models import Count

# Create your views here.
def admin_home(request):
    return render(request,'admin-home.html')

def adminListCategory(request):
    if request.method == 'POST':
        # Handle the form submission from the modal.
        category_id = request.POST.get('category_id')
        category_name = request.POST.get('category_name')
        slug = request.POST.get('slug')
        description = request.POST.get('description')

        category = Category.objects.get(pk=category_id)
        category.category_name = category_name
        category.slug = slug
        category.description = description
        category.save()

        # Return a success response (you can handle errors as needed).
        return JsonResponse({'status': 'success'})

    categories = Category.objects.annotate(product_count=Count('product'))
    context = {
        'categories': categories,
    }
    return render(request, 'adcattabcop.html', context)

def adminAddCategory(request):
    if request.method == 'POST':
        category_name   = request.POST.get('category_name')
        slug            = request.POST.get('slug')
        description     = request.POST.get('description')
        image  = request.FILES.get('image')

        category = Category.objects.create(
            category_name = category_name,
            slug = slug,
            description = description,
            category_image = image
        )

        return redirect('category-list')

    return render(request,'adminAddCategory.html')

def admin_add_products(request):
    
    categories = Category.objects.all()
    
    if request.method == 'POST':
        product_name    = request.POST.get('product_name')
        slug            = request.POST.get('slug')
        category_id     = request.POST.get('category')
        description     = request.POST.get('description')
        old_price       = request.POST.get('old_price')
        new_price       = request.POST.get('new_price')
        stock           = request.POST.get('stock')
        is_available    = request.POST.get('is_available')
        image = request.FILES.get('image')
        
        
        category      = Category.objects.get(pk=category_id)

        product = Product.objects.create(
            product_name = product_name,
            slug=slug,
            description=description,
            old_price = old_price,
            new_price=new_price,
            stock=stock,
            is_available = is_available,
            category=category,
            images=image
        )

        return redirect('product-table')
    
    context = {
        'categories' : categories
    }
    
    return render(request,'adminAddProduct.html',context)




def adminProductTable(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        'products':products,
        "categories":categories
    }
    return render(request,'adminProductTable.html',context)