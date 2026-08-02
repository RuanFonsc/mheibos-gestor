from django.db import models
from django.contrib.auth.hashers import identify_hasher, make_password


class CategoriaProduto(models.TextChoices):
    PAINEL = "PAINEL", "Painel"
    BOLSA = "BOLSA", "Bolsa"
    GRAFICA_RAPIDA = "GRAFICA_RAPIDA", "Grafica rapida"
    COMUNICACAO_VISUAL = "COMUNICACAO_VISUAL", "Comunicacao visual"
    OUTROS = "OUTROS", "Outros"


class UnidadeMedida(models.TextChoices):
    UNIDADE = "UN", "Unidade"
    METRO = "M", "Metro"
    METRO_QUADRADO = "M2", "Metro quadrado"
    FOLHA = "FOLHA", "Folha"
    SERVICO = "SERVICO", "Servico"


class CategoriaServico(models.Model):
    nome = models.CharField(max_length=80, unique=True)
    ativa = models.BooleanField(default=True)
    ordem = models.PositiveIntegerField(default=0)
    alerta_prazo_ativo = models.BooleanField(default=True)
    alerta_dias_uteis = models.PositiveIntegerField(default=2)
    alerta_mesmo_dia_apos_14h = models.BooleanField(default=False)

    class Meta:
        ordering = ["ordem", "nome"]

    def __str__(self):
        return self.nome


class ProdutoServico(models.Model):
    nome = models.CharField(max_length=180, unique=True)
    categoria_servico = models.ForeignKey(
        CategoriaServico,
        related_name="produtos",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    categoria = models.CharField(
        max_length=32,
        choices=CategoriaProduto.choices,
        default=CategoriaProduto.OUTROS,
    )
    unidade = models.CharField(
        max_length=16,
        choices=UnidadeMedida.choices,
        default=UnidadeMedida.UNIDADE,
    )
    preco_venda_padrao = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    custo_estimado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    prazo_entrega_dias_uteis = models.PositiveIntegerField(default=0)
    ativo = models.BooleanField(default=True)
    origem_legado = models.CharField(max_length=80, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nome"]
        indexes = [
            models.Index(fields=["categoria", "ativo"]),
            models.Index(fields=["nome"]),
        ]

    def __str__(self):
        return self.nome


class PreferenciaUI(models.Model):
    chave = models.CharField(max_length=64, unique=True, default="global")
    dados = models.JSONField(default=dict, blank=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Preferência de interface"
        verbose_name_plural = "Preferências de interface"

    def __str__(self):
        return self.chave


class PapelOperador(models.TextChoices):
    ADMIN_GERAL = "ADMIN_GERAL", "Administrador geral"
    ADMIN = "ADMIN", "Administrador"
    USUARIO = "USUARIO", "Usuario"
    TEMPORARIO = "TEMPORARIO", "Usuario temporario"


class CanalAtendimento(models.TextChoices):
    PRESENCIAL = "PRESENCIAL", "Presencial"
    ONLINE = "ONLINE", "Online"


class CategoriaUsuario(models.Model):
    nome = models.CharField(max_length=80, unique=True)
    descricao = models.CharField(max_length=180, blank=True)
    ativa = models.BooleanField(default=True)
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["ordem", "nome"]

    def __str__(self):
        return self.nome


class OperadorGestor(models.Model):
    codigo_origem_offline = models.CharField(
        max_length=12, null=True, blank=True, unique=True
    )
    nome = models.CharField(max_length=80, unique=True)
    foto = models.ImageField(upload_to="usuarios/fotos/", blank=True)
    senha = models.CharField(max_length=128, default="1234")
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=32, blank=True)
    cargo = models.CharField(max_length=120, blank=True)
    papel = models.CharField(
        max_length=24,
        choices=PapelOperador.choices,
        default=PapelOperador.USUARIO,
    )
    categoria_usuario = models.ForeignKey(
        CategoriaUsuario,
        related_name="usuarios",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    canal_atendimento_padrao = models.CharField(
        max_length=16,
        choices=CanalAtendimento.choices,
        default=CanalAtendimento.PRESENCIAL,
    )
    observacoes = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if self.senha:
            try:
                identify_hasher(self.senha)
            except ValueError:
                self.senha = make_password(self.senha)
                update_fields = kwargs.get("update_fields")
                if update_fields is not None:
                    kwargs["update_fields"] = set(update_fields) | {"senha"}
        return super().save(*args, **kwargs)

    @property
    def is_admin_geral(self):
        return self.papel == PapelOperador.ADMIN_GERAL

    @property
    def is_admin(self):
        return self.papel in {PapelOperador.ADMIN_GERAL, PapelOperador.ADMIN}

    @property
    def pode_cancelar_pedido(self):
        return self.is_admin

    @property
    def pode_gerenciar_usuarios(self):
        return self.is_admin

    @property
    def pode_excluir_categoria_servico(self):
        return self.is_admin

    @property
    def pode_criar_categoria_servico(self):
        return self.is_admin

    @property
    def pode_acessar_crm(self):
        return self.is_admin

    @property
    def pode_ver_financeiro_geral(self):
        return self.is_admin

    @property
    def pode_excluir_produto(self):
        return self.papel != PapelOperador.TEMPORARIO


class ChaveRecuperacaoSenha(models.Model):
    chave_hash = models.CharField(max_length=64, unique=True)
    criada_em = models.DateTimeField(auto_now_add=True)
    usada_em = models.DateTimeField(null=True, blank=True)
    criada_por = models.CharField(max_length=80, blank=True)
    observacoes = models.CharField(max_length=180, blank=True)

    class Meta:
        ordering = ["-criada_em"]
        verbose_name = "Chave de recuperacao de senha"
        verbose_name_plural = "Chaves de recuperacao de senha"

    def __str__(self):
        return f"Chave criada em {self.criada_em:%d/%m/%Y %H:%M}"

    @property
    def usada(self):
        return self.usada_em is not None


class PerfilEmpresa(models.Model):
    class LayoutOrdemServico(models.TextChoices):
        A5_DUPLICADO = "A5_DUPLICADO", "A5 duplicada na A4"
        A4_INTEIRA = "A4_INTEIRA", "A4 inteira"

    chave = models.CharField(max_length=64, unique=True, default="global")
    nome_fantasia = models.CharField(max_length=180, blank=True)
    razao_social = models.CharField(max_length=180, blank=True)
    cnpj = models.CharField(max_length=32, blank=True)
    telefone = models.CharField(max_length=32, blank=True)
    telefone_secundario = models.CharField(max_length=32, blank=True)
    telefone_terciario = models.CharField(max_length=32, blank=True)
    instagram = models.CharField(max_length=120, blank=True)
    instagram_secundario = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    endereco = models.TextField(blank=True)
    logo = models.ImageField(upload_to="empresa/", blank=True)
    observacoes = models.TextField(blank=True)
    os_layout = models.CharField(
        max_length=24,
        choices=LayoutOrdemServico.choices,
        default=LayoutOrdemServico.A5_DUPLICADO,
    )
    os_cor_linhas = models.CharField(max_length=7, default="#a9bcff")
    os_cor_textos = models.CharField(max_length=7, default="#06143d")
    os_cor_legendas = models.CharField(max_length=7, default="#06143d")
    os_linha_cabecalho = models.JSONField(default=dict, blank=True)
    os_campos = models.JSONField(default=dict, blank=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Perfil da empresa"
        verbose_name_plural = "Perfil da empresa"

    def __str__(self):
        return self.nome_fantasia or "Perfil da empresa"
