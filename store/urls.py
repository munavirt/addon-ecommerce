from django.urls import path
from . import views
urlpatterns = [ 
    path('',views.home,name='home'),
    path('search/',views.search,name='search'), 
    path('store/',views.store,name='store'),
    path('store/<slug:store_slug>/',views.store,name='products_by_category'),
    path('store/<slug:store_slug>/<slug:product_slug>/',views.product_details,name='product_details'),
    path('whatsapp/<int:product_id>/', views.send_whatsapp_message, name='send_whatsapp_message'),
    path('contact/',views.contact_us,name='contact-us')

]