from django.db import models

# Blocos
class Bloco(models.Model):
    nome_bloco = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_bloco


class Rack(models.Model):
    num_patrimonio = models.CharField(max_length=50, unique=True)
    localizacao = models.CharField(max_length=100)

    def __str__(self):
        return f"Rack {self.num_patrimonio} - {self.localizacao}"


class Switch(models.Model):
    num_patrimonio = models.CharField(max_length=50, unique=True)
    quantidade_portas = models.IntegerField()
    id_rack = models.ForeignKey(Rack, on_delete=models.CASCADE)

    def __str__(self):
        return f"Switch {self.num_patrimonio} ({self.quantidade_portas} portas)"


class Porta(models.Model):
    switch = models.ForeignKey(Switch, related_name="portas", on_delete=models.CASCADE)
    numero = models.IntegerField()
    valor = models.CharField(max_length=100, blank=True, null=True)  # ex: IP, host, etc.

    def __str__(self):
        return f"Porta {self.numero} - {self.valor or 'vazia'}"


# Histórico
class Historico(models.Model):
    acao = models.CharField(max_length=255)
    observacao = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ação: {self.acao} ({self.criado_em:%d/%m/%Y %H:%M})"
