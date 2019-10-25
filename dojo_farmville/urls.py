"""dojo_farmville URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from app_dojofarmville import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('registerUser', views.registerUser),
    path('loginUser', views.loginUser),
    path('home', views.home),
    path('profile', views.profile),
    path('postMessage', views.postMessage),
    path('removeMessage/<messageId>', views.removeMessage),
    path('postComment', views.postComment),
    path('removeComment/<commentId>', views.removeComment),
    path('createEvent', views.createEvent),
    path('logout', views.logout),
    path('farm', views.farm),
    path('grow', views.grow),
    path('pick', views.pick),
    path('plantCorn', views.plantCorn),
    path('plantWheat', views.plantWheat),
    path('plantCarrot',views.plantCarrot),
    path('plantLeek', views.plantLeek),
    path('plantBlackTomato', views.plantBlackTomato),
    path('buyLand',views.buyLand),
    path('buyCorn', views.buyCorn),
    path('buyWheat', views.buyWheat),
    path('buyCarrot', views.buyCarrot),
    path('buyLeek', views.buyLeek),
    path('buyBlackTomato', views.buyBlackTomato),
    path('buyBadge', views.buyBadge)
]
