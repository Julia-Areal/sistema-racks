from django.db import models
from django.contrib.auth.models import User


class Bloco(models.Model):
    nome_bloco = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_bloco


class Rack(models.Model):
    id = models.AutoField(primary_key=True)
    num_patrimonio = models.CharField(max_length=50, unique=True)
    # localizacao = models.CharField(max_length=100)
    capacidade_u = models.IntegerField()
    sala = models.CharField(max_length=100)
    id_bloco = models.ForeignKey(Bloco, on_delete=models.CASCADE, related_name="racks")

    def __str__(self):
        return f"Rack {self.num_patrimonio} - {self.localizacao}"


class Switch(models.Model):
    id = models.AutoField(primary_key=True)
    num_patrimonio = models.CharField(max_length=50, unique=True)
    quantidade_portas = models.IntegerField()
    id_rack = models.ForeignKey(Rack, on_delete=models.CASCADE, related_name="switches")

    def __str__(self):
        return f"Switch {self.num_patrimonio} ({self.quantidade_portas} portas)"


class Porta(models.Model):
    switch = models.ForeignKey(Switch, related_name="portas", on_delete=models.CASCADE)
    numero = models.PositiveIntegerField()
    valor = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Porta {self.numero} - {self.valor or 'vazia'}"


class Historico(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    acao = models.CharField(max_length=255)
    modelo = models.CharField(max_length=50, null=True, blank=True)  # Ex: "Rack", "Switch", "Porta"
    objeto_id = models.IntegerField(null=True, blank=True)  # PK do objeto
    observacao = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.criado_em:%d/%m/%Y %H:%M}] {self.usuario} -> {self.acao}"
