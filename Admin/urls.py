from django.urls import path
from . import views
urlpatterns = [
    path('',views.admin_home,name='admin-home'),
    path('add-category/',views.adminAddCategory,name='add-category'),
    path('category-table/',views.adminListCategory,name='category-list'),
    path('add-product/',views.admin_add_products,name='add-product'),
    path('product-table/',views.adminProductTable,name='product-table')
]