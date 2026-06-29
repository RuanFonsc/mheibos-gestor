from django.db import models


class StatusCadastroCliente(models.TextChoices):
    CADASTRADO = "CADASTRADO", "Cliente cadastrado"
    NAO_CADASTRADO = "NAO_CADASTRADO", "Cliente nao cadastrado"


class Cliente(models.Model):
    nome = models.CharField(max_length=180)
    email = models.EmailField(blank=True)
    telefone_principal = models.CharField(max_length=32, blank=True)
    telefone_secundario = models.CharField(max_length=32, blank=True)
    cpf_cnpj = models.CharField(max_length=32, blank=True)
    endereco = models.TextField(blank=True)
    observacoes = models.TextField(blank=True)
    status_cadastro = models.CharField(
        max_length=20,
        choices=StatusCadastroCliente.choices,
        default=StatusCadastroCliente.NAO_CADASTRADO,
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nome"]
        indexes = [
            models.Index(fields=["nome"]),
            models.Index(fields=["telefone_principal"]),
            models.Index(fields=["status_cadastro", "nome"]),
        ]

    def __str__(self):
        return self.nome
