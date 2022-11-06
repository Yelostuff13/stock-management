"""stock URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from xml.dom.minidom import Document
from django.contrib import admin
from django.urls import path
from store import views
from django.conf.urls.static import static
from django.conf import settings

# from workon.stock.store.views import index



urlpatterns = [
    path('admin/', admin.site.urls),
    path('product/',views.product),
    path('',views.index,name="home"),
    path('Product/<slug:product_slug>',views.index,name="Film_by_product"),
    path('Film/<slug:product_slug>/<slug:Film_slug>',views.index,name="Film_by_product"),
    path('cart/add/<int:film_id>',views.addCart,name="addCart"),
    path('cartdetail',views.cartdetail,name="cartdetail"),
    path('cart/remove/<int:film_id>',views.removeCart,name="removeCart"),
    path('search/',views.search,name='search'),
    path('checkout/',views.CheckOut,name='checkout'),
    path('thankyou/',views.thankyou,name='thankyou')
]

if settings.DEBUG :
    #static/media
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
