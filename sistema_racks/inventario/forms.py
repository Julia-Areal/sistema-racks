from django import forms
from .models import Rack, Switch, Porta
from django.forms import modelformset_factory

class RackForm(forms.ModelForm):
    class Meta:
        model = Rack
        fields = ["num_patrimonio", "capacidade_u", "sala", "id_bloco"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['num_patrimonio'].widget.attrs.update({'class': 'form-control'})
        self.fields['capacidade_u'].widget.attrs.update({'class': 'form-control'})
        self.fields['sala'].widget.attrs.update({'class': 'form-control'})
        self.fields['id_bloco'].widget.attrs.update({'class': 'form-control'})

class SwitchForm(forms.ModelForm):
    class Meta:
        model = Switch
        fields = [
            "num_patrimonio", "quantidade_portas", "endereco_ip",
            "mac_address", "hostname", "modelo", "descricao",
            "principal", "id_rack", "orientacao"
        ]


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
