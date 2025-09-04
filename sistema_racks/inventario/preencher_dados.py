from inventario.models import Bloco

def run():
    Bloco.objects.bulk_create([
        Bloco(nome_bloco="B001"),
        Bloco(nome_bloco="B002"),
        Bloco(nome_bloco="B003"),
    ])
