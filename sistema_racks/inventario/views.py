from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_POST
from .models import Rack, Switch, Porta, Historico, Bloco
from .forms import RackForm, SwitchForm, PortaFormSet
from .utils import registrar_historico

# request handlers

# ---------------------------
# Home
# ---------------------------
@login_required
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
    blocos = Bloco.objects.all()

    q = request.GET.get("q")
    bloco_id = request.GET.get("bloco")
    capacidade_min = request.GET.get("capacidade")

    if q:
        racks = racks.filter(num_patrimonio__icontains=q) | racks.filter(sala__icontains=q)
    if bloco_id:
        racks = racks.filter(id_bloco__id=bloco_id)
    if capacidade_min:
        racks = racks.filter(capacidade_u__gte=capacidade_min)

    return render(request, "rack_list.html", {"racks": racks, "blocos": blocos})

@login_required
@registrar_historico("Criação de Rack", "Rack")
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
@registrar_historico("Edição de Rack", "Rack")
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
@registrar_historico("Deleção de Rack", "Rack")
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
    racks = Rack.objects.all()
    blocos = Bloco.objects.all()

    q = request.GET.get("q")
    portas = request.GET.get("portas")
    rack_id = request.GET.get("rack")
    bloco_id = request.GET.get("bloco")

    if q:
        switches = switches.filter(num_patrimonio__icontains=q)
    if portas:
        switches = switches.filter(quantidade_portas__gte=portas)
    if rack_id:
        switches = switches.filter(id_rack__id=rack_id)
    if bloco_id:
        switches = switches.filter(id_rack__id_bloco__id=bloco_id)

    return render(request, "switch_list.html", {
        "switches": switches,
        "racks": racks,
        "blocos": blocos,
    })

@login_required
@registrar_historico("Criação de Switch", "Switch")
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
@registrar_historico("Edição de Switch", "Switch")
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
@registrar_historico("Deleção de Switch", "Switch")
def switch_delete(request, pk):
    switch = get_object_or_404(Switch, pk=pk)
    if request.method == "POST":
        switch.delete()
        return redirect("switch_list")
    return render(request, "confirm_delete.html", {"obj": switch, "type": "Switch"})

@login_required
def switches_por_rack(request, rack_id):
    rack = get_object_or_404(Rack, pk=rack_id)
    switches = Switch.objects.filter(id_rack=rack)
    return render(request, "switch_list_por_rack.html", {
        "rack": rack,
        "switches": switches,
    })

@login_required
@registrar_historico("Edição de Portas do Switch", "Switch")
def salvar_portas_switch(request, switch_id):
    switch = get_object_or_404(Switch, id=switch_id)
    if request.method == "POST":
        for porta in switch.portas.all():
            novo_valor = request.POST.get(f"porta_{porta.id}")
            porta.valor = novo_valor
            porta.save()
        return redirect("switch_detail", pk=switch.id)

@login_required
def switch_detail(request, pk):
    switch = get_object_or_404(Switch, pk=pk)
    return render(request, "switch_detail.html", {"switch": switch})

@require_POST
@registrar_historico("Edição de Porta", "Porta")
def porta_update(request, porta_id):
    porta = get_object_or_404(Porta, id=porta_id)
    valor = request.POST.get("valor")
    porta.valor = valor
    porta.save()
    return redirect("switch_list")

@login_required
@registrar_historico("Deleção de Porta", "Porta")
def porta_delete(request, pk):
    porta = get_object_or_404(Porta, pk=pk)
    if request.method == "POST":
        porta.delete()
        # Historico.objects.create(
        #     usuario=request.user,
        #     acao="Exclusão de Porta",
        #     modelo="Porta",
        #     objeto_id=pk,
        #     observacao=f"Porta {pk} excluída"
        # )
        return redirect("porta_list")
    return render(request, "confirm_delete.html", {"obj": porta, "type": "Porta"})

@login_required
def historico_list(request):
    logs = Historico.objects.all().order_by("-criado_em")
    return render(request, "historico_list.html", {"logs": logs})

@login_required
def editar_portas(request, switch_id):
    switch = get_object_or_404(Switch, id=switch_id)
    queryset = Porta.objects.filter(switch=switch).order_by("numero")

    if request.method == "POST":
        formset = PortaFormSet(request.POST, queryset=queryset)
        if formset.is_valid():
            formset.save()
            return redirect("editar_portas", switch_id=switch.id)
    else:
        formset = PortaFormSet(queryset=queryset)

    return render(request, "inventario/editar_portas.html", {
        "switch": switch,
        "formset": formset
    })
