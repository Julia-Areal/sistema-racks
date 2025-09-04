from django.db import models

# Blocos
class Bloco(models.Model):
    nome_bloco = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_bloco


# Racks
class Rack(models.Model):
    num_patrimonio = models.IntegerField(unique=True, null=True, blank=True)
    capacidade_u = models.IntegerField(null=True, blank=True)
    sala = models.CharField(max_length=50, null=True, blank=True)
    bloco = models.ForeignKey(Bloco, on_delete=models.CASCADE, related_name="racks", null="True")

    def __str__(self):
        return f"Rack {self.num_patrimonio or '-'} - {self.sala or 'Sem sala'}"


# Switches
class Switch(models.Model):
    quantidade_portas = models.SmallIntegerField()
    num_patrimonio = models.IntegerField(unique=True, null=True, blank=True)
    rack = models.ForeignKey(Rack, on_delete=models.CASCADE, related_name="switches")

    def __str__(self):
        return f"Switch {self.num_patrimonio or '-'} ({self.quantidade_portas} portas)"


# Portas
class Porta(models.Model):
    numero = models.PositiveIntegerField()  # número da porta no switch
    switch = models.ForeignKey(Switch, on_delete=models.CASCADE, related_name="portas")

    def __str__(self):
        return f"Porta {self.numero} - Switch {self.switch.num_patrimonio}"


# Histórico
class Historico(models.Model):
    acao = models.CharField(max_length=255)
    observacao = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ação: {self.acao} ({self.criado_em:%d/%m/%Y %H:%M})"
