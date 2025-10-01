from django.urls import path
from . import views

urlpatterns = [
    # path("", views.home, name="home"),
    # Autenticação
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Racks
    path("racks/", views.rack_list, name="rack_list"),
    path("racks/novo/", views.rack_create, name="rack_create"),
    path("racks/<int:pk>/editar/", views.rack_update, name="rack_update"),
    path("racks/<int:pk>/excluir/", views.rack_delete, name="rack_delete"),
    path("racks/<int:rack_id>/switches/", views.switches_por_rack, name="switches_por_rack"),

    # Switches
    path("switches/", views.switch_list, name="switch_list"),
    path("switches/novo/", views.switch_create, name="switch_create"),
    path("switches/<int:pk>/editar/", views.switch_update, name="switch_update"),
    path("switches/<int:pk>/excluir/", views.switch_delete, name="switch_delete"),
    path("porta/<int:porta_id>/update/", views.porta_update, name="porta_update"),
    path("switch/<int:switch_id>/salvar_portas/", views.salvar_portas_switch, name="salvar_portas_switch"),
    path("switch/<int:pk>/", views.switch_detail, name="switch_detail"),
    path("switch/<int:switch_id>/portas/", views.editar_portas, name="editar_portas"),

    # Histórico
    path("historico/", views.historico_list, name="historico_list"),

]
