"""
URL configuration for Touristproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from Touristapp.views import packageview,travel_agencyview,packagedetail,package,deletepackege,detailpackage
from Touristapp import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',travel_agencyview.as_view(),name="index"),
    path('packageview/',packageview.as_view(), name="packageview"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('travellogin/',views.travellogin,name="travellogin"),
    path('travelregister/',views.travelregister,name="travelregister"),
    path('packagedetail/<int:pk>',packagedetail.as_view(),name="packagedetail"),
    path('search/',views.search,name="search"),
    path('addtocart/',views.addtocart,name="addtocart"),
    path('viewcart/',views.viewcart,name="viewcart"),
    path('removepacakge/', views.removepacakge, name='removepacakge'),
    path('summarypage',views.summary,name='summary'),
    path('placeorder/',views.placeorder, name="placeorder"),
    path('success',views.success,name='success'),
    path('payment/',views.payment,name="payment"),
    path('logout/',views.logout,name="logout"),
    path('travelnavbar/',views.travel_agencynavbar,name='travelnavbar'),
    path('profile/',views.travel_agencyprofile,name='profile'),
    path('traveleditprofile/',views.traveleditprofile,name='traveleditprofile'), 
    path('addpackage',views.addpackage,name='addpackage'),
    path('viewpacakge/',views.viewpacakge,name='viewpacakge'),
     path('deletepacakge/<int:pk>',deletepackege.as_view(),name='deletepackege'),
    path('editpacakge/<int:pk>',views.editpacakge,name='editpacakge'),
    path('travellogout',views.travel_agencylogout,name='travellogout'),
     path('my_order/', views.my_order, name='my_order')

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)