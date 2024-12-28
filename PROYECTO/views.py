from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from .models import Producto, CarritoItem, MetaPersonal, Plan, UserPlan
from django.http import JsonResponse
from django.contrib import messages
from .forms import CustomUserChangeForm, CustomUserCreationForm


# Create your views here.


def home(request):
    return render(request, 'home.html')

def tuespacio(request):
    return render(request, 'espacio/home1.html')

def home1(request):
    user_planes = UserPlan.objects.filter(user=request.user)
    return render(request, 'espacio/home1.html', {'user_planes': user_planes})

def planes(request):
                                
    planes = Plan.objects.all()
    user_planes = UserPlan.objects.filter(user=request.user)
    planes_disponibles = planes.exclude(id__in=user_planes.values_list('plan_id', flat=True)) # Excluir los planes a los que el usuario ya se ha unido
    return render(request, 'espacio/miplan.html', {'planes': planes_disponibles, 'user_planes': user_planes})

def unirse_a_plan(request, plan_id):
    
    if UserPlan.objects.filter(user=request.user).exists():# Verificar si el usuario ya tiene un plan
        messages.error(request, "Ya tienes un plan en curso. No puedes unirte a otro.")
        return redirect('miplan')
    
    
    plan = get_object_or_404(Plan, id=plan_id)
    user_plan, created = UserPlan.objects.get_or_create(user=request.user, plan=plan)
    if created:
        messages.success(request, f"Te has unido al plan {plan.nombre}.")
    return redirect('miplan')

def perfil(request):
    return render(request, 'espacio/perfil.html')

def editar_perfil(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado con éxito.')
            return redirect('perfil')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'espacio/editar_perfil.html', {'form': form})

def cambiar_contraseña(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, '¡Tu contraseña ha sido actualizada exitosamente!')
            return redirect('perfil') 
        else:
            messages.error(request, 'Por favor corrige los errores a continuación.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'espacio/cambiar_contraseña.html', {'form': form})
    
def productos(request):

    productos = Producto.objects.all()
    return render(request, 'productos.html', {'productos' : productos})





def carrito(request):
    # Obtener todos los elementos en el carrito del usuario autenticado
    items = CarritoItem.objects.filter(usuario=request.user)
    total = sum(item.subtotal() for item in items)

    return render(request, 'carrito.html', {'items': items, 'total': total})

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    # Verificar si ya existe en el carrito del usuario
    item, created = CarritoItem.objects.get_or_create(producto=producto, usuario=request.user)
    if not created:
        item.cantidad += 1
    messages.success(request, '¡Producto agregado!')
    item.save()
    
    
    if request.META['HTTP_REFERER']:
        if 'carrito' in request.META['HTTP_REFERER']:
            return redirect('carrito')
        elif 'productos' in request.META['HTTP_REFERER']:
            return redirect('productos')
    
    return redirect('productos')

def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id, usuario=request.user)
    if item.cantidad > 1:
        item.cantidad -= 1
        item.save()
    else:
        item.delete()
    return redirect('carrito')

def comprar(request):
    items = CarritoItem.objects.filter(usuario=request.user)
    items.delete()  # Limpiar carrito
    messages.success(request, 'Compra realizada con éxito.')
    return redirect('home')# aqui va la pag de medio de pago













def metapersonal(request):
    if request.method == 'POST':
        altura = request.POST.get('altura')
        peso = request.POST.get('peso')
        meta = request.POST.get('meta')

        # Guardar los datos en la base de datos con el usuario autenticado
        metapersonal = MetaPersonal(altura=altura, peso=peso, meta=meta)
        metapersonal.save(usuario=request.user)

        messages.success(request, '¡Tu meta personal ha sido enviada exitosamente!')

        return redirect('home')

    return render(request, 'metapersonal.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form' : UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                k = Group.objects.get(name='user')
                user.groups.add(k)
                user.save()
                login(request, user)
                return redirect('home')
            except:
                return render(request, 'signup.html', {
                    'form' : UserCreationForm,
                    "error" : 'usuario ya existe'
                })
        return render(request, 'signup.html', {
            'form' : UserCreationForm,
            "error" : 'contraseñas no coinciden'
        })

    
def signout(request):
    
    logout(request)
    return redirect('home')
                
def signin(request):
    if request.method == "GET":
        return render(request, 'signin.html',{
        'form' : AuthenticationForm
    })
        
    else:
        user = authenticate(request, username=request.POST ['username'], password=request.POST ['password'])
        if user is None:
            return render(request, 'signin.html',{
                'form' : AuthenticationForm,
                'error' : 'Nombre o contraseña incorrectos'
            })
        
        else:
            login(request, user)
            return redirect('home')

def listar_metas(request):
    metas = MetaPersonal.objects.all()
    return render(request, 'listar_metas.html', {'metas': metas})

def salir_de_plan(request, plan_id):
    user_plan = get_object_or_404(UserPlan, user=request.user, plan_id=plan_id)
    user_plan.delete()
    messages.success(request, 'Te has salido del plan exitosamente.')
    return redirect('home1')

def actualizar_perfil(request):
    if request.method == 'POST':
        
        password_anterior = request.POST.get('password_anterior')
        user = authenticate(username=request.user.username, password=password_anterior)

        if user is not None:
            # Actualizar el nombre del usuario
            
            request.user.last_name = request.POST.get('username', request.user.username)

            # Actualizar la contraseña
            nueva_contraseña = request.POST.get('password1')
            if nueva_contraseña:
                request.user.set_password(nueva_contraseña)

            request.user.save()
            messages.success(request, 'Perfil actualizado con éxito.')
            return redirect('perfil')
        else:
            messages.error(request, 'Contraseña anterior incorrecta.')

    return render(request, 'espacio/home.html', {'form': request.user})








        