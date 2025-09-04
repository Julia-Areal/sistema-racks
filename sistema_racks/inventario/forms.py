from django import forms
from .models import Rack, Switch

class RackForm(forms.ModelForm):
    class Meta:
        model = Rack
        fields = "__all__"

class SwitchForm(forms.ModelForm):
    class Meta:
        model = Switch
        fields = "__all__"
