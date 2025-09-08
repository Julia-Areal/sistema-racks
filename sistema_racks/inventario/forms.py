from django import forms
from .models import Rack, Switch, Porta
from django.forms import modelformset_factory

class PortaForm(forms.ModelForm):
    class Meta:
        model = Porta
        fields = ["valor"]

PortaFormSet = modelformset_factory(
    Porta,
    form=PortaForm,
    extra=0,  # não cria linhas extras
    can_delete=False
)

class RackForm(forms.ModelForm):
    class Meta:
        model = Rack
        fields = ["id", "num_patrimonio", "capacidade_u", "sala", "id_bloco"]

class SwitchForm(forms.ModelForm):
    class Meta:
        model = Switch
        fields = ["id", "num_patrimonio", "quantidade_portas", "id_rack"]
