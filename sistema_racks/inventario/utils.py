from functools import wraps
from .models import Historico

def registrar_historico(acao, modelo=None):
    """
    Decorador para registrar ações no histórico automaticamente.
    Exemplo de uso:
    @registrar_historico("Criação de Rack", "Rack")
    def rack_create(request): ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            response = view_func(request, *args, **kwargs)

            # só registra se o request foi POST bem-sucedido
            if request.method == "POST" and response.status_code in (302, 200):
                objeto_id = kwargs.get("pk", None)  # tenta pegar id da URL se existir
                Historico.objects.create(
                    usuario=request.user if request.user.is_authenticated else None,
                    acao=acao,
                    modelo=modelo,
                    objeto_id=objeto_id,
                    observacao=f"Ação '{acao}' executada no modelo {modelo}"
                )
            return response
        return _wrapped_view
    return decorator
