from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_POST
from .models import Rack, Switch, Porta
from .forms import RackForm, SwitchForm

# resquest handlers

# ---------------------------
# Home
# ---------------------------
def home(request):
    return render(request, "home.html")

# ---------------------------
# Autenticação
# ---------------------------
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")

# ---------------------------
# Racks
# ---------------------------
@login_required
def rack_list(request):
    racks = Rack.objects.all()
    return render(request, "rack_list.html", {"racks": racks})

@login_required
def rack_create(request):
    if request.method == "POST":
        form = RackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("rack_list")
    else:
        form = RackForm()
    return render(request, "rack_form.html", {"form": form})

@login_required
def rack_update(request, pk):
    rack = get_object_or_404(Rack, pk=pk)
    if request.method == "POST":
        form = RackForm(request.POST, instance=rack)
        if form.is_valid():
            form.save()
            return redirect("rack_list")
    else:
        form = RackForm(instance=rack)
    return render(request, "rack_form.html", {"form": form})

@login_required
def rack_delete(request, pk):
    rack = get_object_or_404(Rack, pk=pk)
    if request.method == "POST":
        rack.delete()
        return redirect("rack_list")
    return render(request, "confirm_delete.html", {"obj": rack, "type": "Rack"})

# ---------------------------
# Switches
# ---------------------------
@login_required
def switch_list(request):
    switches = Switch.objects.all()
    return render(request, "switch_list.html", {"switches": switches})

@login_required
def switch_create(request):
    if request.method == "POST":
        form = SwitchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("switch_list")
    else:
        form = SwitchForm()
    return render(request, "switch_form.html", {"form": form})

@login_required
def switch_update(request, pk):
    switch = get_object_or_404(Switch, pk=pk)
    if request.method == "POST":
        form = SwitchForm(request.POST, instance=switch)
        if form.is_valid():
            form.save()
            return redirect("switch_list")
    else:
        form = SwitchForm(instance=switch)
    return render(request, "switch_form.html", {"form": form})

@login_required
def switch_delete(request, pk):
    switch = get_object_or_404(Switch, pk=pk)
    if request.method == "POST":
        switch.delete()
        return redirect("switch_list")
    return render(request, "confirm_delete.html", {"obj": switch, "type": "Switch"})

@require_POST
def porta_update(request, porta_id):
    porta = get_object_or_404(Porta, id=porta_id)
    valor = request.POST.get("valor")
    porta.valor = valor
    porta.save()
    return redirect("switch_list")
