from functools import wraps
from .models import Historico

def registrar_historico(acao, item=None):
    """
    Decorador para registrar ações no histórico automaticamente.
    Exemplo:
    @registrar_historico("Criação de Rack", "Rack")
    def rack_create(request): ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            response = view_func(request, *args, **kwargs)

            if request.method == "POST" and response.status_code in (200, 302):
                objeto_id = (
                    kwargs.get("pk")
                    or kwargs.get("id")
                    or kwargs.get("rack_id")
                    or kwargs.get("switch_id")
                )

                Historico.objects.create(
                    usuario=request.user,
                    acao=acao,
                    item=item,
                    observacao=f"Ação '{acao}' executada no modelo {item}"
                )
            return response
        return _wrapped_view
    return decorator
