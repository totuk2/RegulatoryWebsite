from django.urls import path
from . import views

app_name = 'website'
urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.ma_overview, name='product_overview'),
    path('products/<int:ma_number>', views.ma_detail, name='product_detail'),
    path('company/', views.company_overview, name='company_overview'),
    path('company/<int:company_id>', views.company_detail, name='comapny_detail'),
]
