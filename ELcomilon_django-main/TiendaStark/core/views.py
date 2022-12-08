from calendar import month
from email import message
from pyexpat.errors import messages
from typing import Awaitable
from datetime import date, datetime
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from .models import  Productos, PerfilUsuario, Ventas 
from .forms import  VehiculoForm, IniciarSesionForm
from .forms import RegistrarUsuarioForm, PerfilUsuarioForm,  CustomUserForm
#from .error.transbank_error import TransbankError
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import get_template
import random

def home(request):
    return render(request, "core/home.html")

def index(request):
    return render(request, "core/index.html")

def iniciar_sesion(request):
    data = {"mesg": "", "form": IniciarSesionForm()}

    if request.method == "POST":
        form = IniciarSesionForm(request.POST)
        if form.is_valid:
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(home)
                else:
                    data["mesg"] = "¡La cuenta o la password no son correctos!"
            else:
                data["mesg"] = "¡La cuenta o la password no son correctos!"
    return render(request, "core/iniciar_sesion.html", data)

def cerrar_sesion(request):
    logout(request)
    return redirect(home)

def tienda(request):
    data = {"list": Productos.objects.all().order_by('patente')}
    return render(request, "core/tienda.html", data)

#https://www.transbankdevelopers.cl/documentacion/como_empezar#como-empezar
#https://www.transbankdevelopers.cl/documentacion/como_empezar#codigos-de-comercio
#https://www.transbankdevelopers.cl/referencia/webpay

# Tipo de tarjeta   Detalle                        Resultado
#----------------   -----------------------------  ------------------------------
# VISA              4051885600446623
#                   CVV 123
#                   cualquier fecha de expiración  Genera transacciones aprobadas.
# AMEX              3700 0000 0002 032
#                   CVV 1234
#                   cualquier fecha de expiración  Genera transacciones aprobadas.
# MASTERCARD        5186 0595 5959 0568
#                   CVV 123
#                   cualquier fecha de expiración  Genera transacciones rechazadas.
# Redcompra         4051 8842 3993 7763            Genera transacciones aprobadas (para operaciones que permiten débito Redcompra y prepago)
# Redcompra         4511 3466 6003 7060            Genera transacciones aprobadas (para operaciones que permiten débito Redcompra y prepago)
# Redcompra         5186 0085 4123 3829            Genera transacciones rechazadas (para operaciones que permiten débito Redcompra y prepago)

@csrf_exempt
def iniciar_pago(request, id):
    print("Webpay Plus Transaction.create")
    buy_order = str(random.randrange(1000000, 99999999))
    session_id = request.user.username
    amount = Productos.objects.get(patente=id).precio
    return_url = 'http://127.0.0.1:8000/pago_exitoso/'

    # response = Transaction.create(buy_order, session_id, amount, return_url)
    commercecode = "597055555532"
    apikey = "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C"

    tx = Transaction(options=WebpayOptions(commerce_code=commercecode, api_key=apikey, integration_type="TEST"))
    response = tx.create(buy_order, session_id, amount, return_url)
    print(response['token'])

    

    context = {
        "buy_order": buy_order,
        "session_id": session_id,
        "amount": amount,
        "return_url": return_url,
        "response": response,
        "token_ws": response['token'],
        "url_tbk": response['url'],
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "email": request.user.email,
        
    }

    return render(request, "core/iniciar_pago.html", context)

@csrf_exempt
def pago_exitoso(request):

    if request.method == "GET":
        token = request.GET.get("token_ws")
        print("commit for token_ws: {}".format(token))
        commercecode = "597055555532"
        apikey = "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C"
        tx = Transaction(options=WebpayOptions(commerce_code=commercecode, api_key=apikey, integration_type="TEST"))
        response = tx.commit(token=token)
        print("response: {}".format(response))

        user = User.objects.get(username=response['session_id'])
        form = PerfilUsuarioForm()

        context = {
            "buy_order": response['buy_order'],
            "session_id": response['session_id'],
            "amount": response['amount'],
            "response": response,
            "token_ws": token,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "response_code": response['response_code']
        }
#Enviar info. de registro de compra
        registrar_venta(context["buy_order"], user.first_name, user.last_name, context["email"], context["amount"])
            
        return render(request, "core/pago_exitoso.html", context)
    else:
        return redirect(home)
    
#METODO DE REGISTRO
@csrf_exempt
def registrar_venta(orden, nombre, apellido, correo, monto):

    nueva_venta = Ventas()
    nueva_venta.orden_compra = orden
    nueva_venta.nombre = nombre
    nueva_venta.apellido = apellido
    nueva_venta.correo = correo
    nueva_venta.monto = monto
    nueva_venta.fecha_compra = date.today()
    nueva_venta.save()

    return nueva_venta

@csrf_exempt
def ficha(request, id):
    data = {"mesg": "", "producto": None}

    if request.method == "POST":
        if request.user.is_authenticated and not request.user.is_staff:
            return redirect(iniciar_pago, id)
        else:
            data["mesg"] = "¡Para poder comprar debe iniciar sesión como cliente!"

    data["producto"] = Productos.objects.get(patente=id)
    return render(request, "core/ficha.html", data)
 
@csrf_exempt
def administrar_productos(request, action, id):
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect(home)

    data = {"mesg": "", "form": VehiculoForm, "action": action, "id": id, "formsesion": IniciarSesionForm}

    if action == 'ins':
        if request.method == "POST":
            form = VehiculoForm(request.POST, request.FILES)
            if form.is_valid:
                try:
                    form.save()
                    data["mesg"] = "¡El producto fue creado correctamente!"
                except:
                    data["mesg"] = "¡No se pueden crear dos producto con la misma id!"

    elif action == 'upd':
        objeto = Productos.objects.get(patente=id)
        if request.method == "POST":
            form = VehiculoForm(data=request.POST, files=request.FILES, instance=objeto)
            if form.is_valid:
                form.save()
                data["mesg"] = "¡El producto fue actualizado correctamente!"
        data["form"] = VehiculoForm(instance=objeto)

    elif action == 'del':
        try:
            Productos.objects.get(patente=id).delete()
            data["mesg"] = "¡El producto fue eliminado correctamente!"
            return redirect(administrar_productos, action='ins', id = '-1')
        except:
            data["mesg"] = "¡El producto ya estaba eliminado!"

    data["list"] = Productos.objects.all().order_by('patente')
    return render(request, "core/administrar_productos.html", data)

def registrar_usuario(request):
    data = {
        'form': CustomUserForm()
    }
    
    if request.method == 'POST':
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data['username']
            rut = request.POST.get("rut")
            direccion = request.POST.get("direccion")
            user = authenticate(username = form.cleaned_data["username"], password=form.cleaned_data["password1"])
            return redirect(iniciar_sesion)
    form = RegistrarUsuarioForm()
    data["form"] = form
    return render(request, "core/registrar_usuario.html", context={'form': form})

def perfil_usuario(request):
    data = {"mesg": "", "form": PerfilUsuarioForm}

    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST)
        if form.is_valid():
            user = request.user
            user.first_name = request.POST.get("first_name")
            user.last_name = request.POST.get("last_name")
            user.email = request.POST.get("email")
            user.save()
            data["mesg"] = "¡Sus datos fueron actualizados correctamente!"

    
    form = PerfilUsuarioForm()
    form.fields['first_name'].initial = request.user.first_name
    form.fields['last_name'].initial = request.user.last_name
    form.fields['email'].initial = request.user.email
    data["form"] = form
    return render(request, "core/perfil_usuario.html", data)


def registro(request):
    data = {
        'form': CustomUserForm()
    }
    
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = form.cleaned_data["username"], password=form.cleaned_data["password1"])
            login(request, user)
            return redirect(to="home")
            data["form"] = form
    return render(request, 'core/registro.html', data)

def reportes(request):
    data = {
        'ventas': Ventas.objects.all(),
        'ventas2': Productos.objects.all()
    }
    return render(request, 'reportes/reporte.html', data)

def reportes_usuarios(request):
    data = {
        'ventas': Ventas.objects.filter(nombre = request.user.first_name)
    }
    return render(request, 'core/reporte_usuarios.html', data)





