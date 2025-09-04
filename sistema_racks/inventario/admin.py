from django.contrib import admin
from .models import Bloco, Rack, Switch, Porta, Historico

admin.site.register(Bloco)
admin.site.register(Rack)
admin.site.register(Switch)
admin.site.register(Porta)
admin.site.register(Historico)
