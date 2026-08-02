from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from math import gcd

from PIL import Image, UnidentifiedImageError


EXTENSOES_RASTER_SUPORTADAS = {
    "bmp",
    "gif",
    "jfif",
    "jpeg",
    "jpg",
    "png",
    "tif",
    "tiff",
    "webp",
}


@dataclass(frozen=True)
class ResultadoMetadadosGraficos:
    aplicavel: bool
    largura_px: int | None = None
    altura_px: int | None = None
    resolucao_dpi: Decimal | None = None
    propriedades: dict = field(default_factory=dict)
    discrepancia: dict | None = None


def _normalizar_dpi(valor) -> Decimal | None:
    if isinstance(valor, (list, tuple)):
        valor = valor[0] if valor else None
    try:
        numero = Decimal(str(valor))
    except (InvalidOperation, TypeError, ValueError):
        return None
    if not numero.is_finite() or numero <= 0 or numero > Decimal("999999.99"):
        return None
    return numero.quantize(Decimal("0.01"))


def extrair_metadados_graficos(caminho: str, extensao: str) -> ResultadoMetadadosGraficos:
    extensao = (extensao or "").strip().lower().lstrip(".")
    if extensao not in EXTENSOES_RASTER_SUPORTADAS:
        return ResultadoMetadadosGraficos(
            aplicavel=False,
            propriedades={
                "extrator": "PILLOW",
                "suportado": False,
                "extensao": extensao,
            },
        )
    try:
        with Image.open(caminho) as imagem:
            largura, altura = imagem.size
            divisor = gcd(largura, altura) if largura and altura else 1
            propriedades = {
                "extrator": "PILLOW",
                "suportado": True,
                "formato": imagem.format or extensao.upper(),
                "modo_cor": imagem.mode,
                "proporcao": f"{largura // divisor}:{altura // divisor}",
            }
            quadros = getattr(imagem, "n_frames", 1)
            if quadros > 1:
                propriedades["quadros"] = quadros
            dpi = _normalizar_dpi(imagem.info.get("dpi"))
            return ResultadoMetadadosGraficos(
                aplicavel=True,
                largura_px=largura,
                altura_px=altura,
                resolucao_dpi=dpi,
                propriedades=propriedades,
            )
    except (Image.DecompressionBombError, UnidentifiedImageError, OSError) as exc:
        return ResultadoMetadadosGraficos(
            aplicavel=True,
            propriedades={
                "extrator": "PILLOW",
                "suportado": True,
                "erro_leitura": type(exc).__name__,
            },
            discrepancia={
                "codigo": "PROPRIEDADES_TECNICAS_INDISPONIVEIS",
                "mensagem": "O arquivo raster existe, mas suas propriedades tecnicas nao puderam ser lidas.",
            },
        )
