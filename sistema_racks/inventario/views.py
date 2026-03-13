from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_POST
from .models import Rack, Switch, Porta, Historico, Bloco
from .forms import RackForm, SwitchForm, PortaFormSet
from .utils import registrar_historico
from django.http import HttpResponse
from odf.opendocument import OpenDocumentSpreadsheet
from odf.style import Style, TextProperties
from odf.table import Table, TableRow, TableCell
from odf.text import P

# request handlers

# ---------------------------
# Autenticação
# ---------------------------
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("rack_list")
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
def switch_create_in_rack(request, rack_id):
    rack = get_object_or_404(Rack, id=rack_id)

    if request.method == "POST":
        form = SwitchForm(request.POST)
        form.fields.pop("id_rack", None)
        if form.is_valid():
            switch = form.save(commit=False)
            switch.id_rack = rack
            switch.save()
            return redirect("switches_por_rack", rack_id=rack.id)
    else:
        form = SwitchForm()
        form.fields.pop("id_rack", None)

    return render(request, "switch_form.html", {
        "form": form,
        "rack": rack
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
def switch_detail(request, pk, rack_id=None):
    switch = get_object_or_404(Switch, pk=pk)
    total = switch.quantidade_portas
    metade = total // 2

    portas_primeira_metade = switch.portas.all()[:metade]
    portas_segunda_metade = switch.portas.all()[metade:]

    return render(request, "switch_detail.html", {
        "switch": switch,
        "rack_id": rack_id,
        "portas_primeira_metade": portas_primeira_metade,
        "portas_segunda_metade": portas_segunda_metade,
    })

@login_required
@require_POST
@registrar_historico("Edição de Porta", "Porta")
def porta_update(request, porta_id):
    porta = get_object_or_404(Porta, id=porta_id)
    valor = request.POST.get("valor")
    porta.valor = valor
    porta.save()
    return redirect("switch_list")

@login_required
def historico_list(request):
    historicos = Historico.objects.all().order_by("-criado_em")
    return render(request, "historico_list.html", {"historicos": historicos})

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

@login_required
def export_rack_ods(request, rack_id):
    rack = Rack.objects.prefetch_related("switches__portas").get(pk=rack_id)

    doc = OpenDocumentSpreadsheet()
    style = Style(name="Bold", family="paragraph")
    style.addElement(TextProperties(fontweight="bold"))
    doc.styles.addElement(style)

    table = Table(name=f"Rack_{rack.num_patrimonio}")

    # Nome do Rack
    row = TableRow()
    cell = TableCell()
    cell.addElement(P(text=f"Rack: {rack.num_patrimonio}", stylename=style))
    row.addElement(cell)
    table.addElement(row)

    for switch in rack.switches.all():
        # Linha com nome do switch
        row = TableRow()
        cell = TableCell()
        cell.addElement(P(text=f"Switch: {switch.num_patrimonio}", stylename=style))
        row.addElement(cell)
        table.addElement(row)

        # Cabeçalho das portas
        header_row = TableRow()
        for col_name in ["Porta", "Valor"]:
            cell = TableCell()
            cell.addElement(P(text=col_name, stylename=style))
            header_row.addElement(cell)
        table.addElement(header_row)

        # Portas
        for porta in switch.portas.all().order_by("numero"):
            row = TableRow()
            cell_num = TableCell()
            cell_num.addElement(P(text=str(porta.numero)))
            row.addElement(cell_num)

            cell_val = TableCell()
            cell_val.addElement(P(text=str(porta.valor) if porta.valor is not None else ""))
            row.addElement(cell_val)

            table.addElement(row)

    doc.spreadsheet.addElement(table)

    response = HttpResponse(content_type="application/vnd.oasis.opendocument.spreadsheet")
    response["Content-Disposition"] = f'attachment; filename="rack_{rack.num_patrimonio}.ods"'
    doc.save(response)

    return response