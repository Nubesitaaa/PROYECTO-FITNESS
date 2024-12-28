"""FITNESS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from PROYECTO import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    path('logout/', views.signout, name="logout"),
    path('signin/', views.signin, name="signin"),
    path('signup/', views.signup, name="signup"),


    path('carrito/', views.carrito, name='carrito'),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('comprar/', views.comprar, name='comprar'),
    path('eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    


    path('productos/', views.productos, name="productos"),
    path('metapersonal/', views.metapersonal, name="metapersonal"),
    path('listar_metas/', views.listar_metas, name="listar_metas"),
    path('tuespacio/', views.tuespacio, name="tuespacio"),

    path('home1/', views.home1, name="home1"),
    path('perfil/', views.perfil, name="perfil"),
    path('actualizar_perfil/', views.actualizar_perfil, name="actualizar_perfil"),
    path('editar_perfil/', views.editar_perfil, name="editar_perfil"),
    path('cambiar_contraseña/', views.cambiar_contraseña, name="cambiar_contraseña"),
    path('miplan/', views.planes, name="miplan"),
    path('unirse_a_plan/<int:plan_id>/', views.unirse_a_plan, name="unirse_a_plan"),
    path('salir_de_plan/<int:plan_id>/', views.salir_de_plan, name='salir_de_plan'),
    


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
