from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    # Autenticação
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Racks
    path("racks/", views.rack_list, name="rack_list"),
    path("racks/novo/", views.rack_create, name="rack_create"),
    path("racks/<int:pk>/editar/", views.rack_update, name="rack_update"),
    path("racks/<int:pk>/excluir/", views.rack_delete, name="rack_delete"),

    # Switches
    path("switches/", views.switch_list, name="switch_list"),
    path("switches/novo/", views.switch_create, name="switch_create"),
    path("switches/<int:pk>/editar/", views.switch_update, name="switch_update"),
    path("switches/<int:pk>/excluir/", views.switch_delete, name="switch_delete"),
]
