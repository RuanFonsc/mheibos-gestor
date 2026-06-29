from django.shortcuts import redirect
from django.http import HttpResponse
from django.urls import reverse
from django.conf import settings

from apps.catalogo.bootstrap import primeiro_admin_pendente
from apps.catalogo.integrity import check_integrity
from apps.catalogo.licensing import enforced, verify_license


def caminho_liberado_licenca(caminho):
    return (
        caminho.startswith("/licenca/")
        or caminho.startswith("/static/")
        or caminho.startswith("/media/")
        or caminho.startswith("/admin/")
        or caminho.startswith("/api/launcher/")
    )


class LicencaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        caminho = request.path_info
        if enforced() and not caminho_liberado_licenca(caminho):
            status = verify_license()
            if not status.ok:
                request.session["licenca_erro"] = status.message
                return redirect(f"{reverse('licenca_ativar')}?next={request.get_full_path()}")
        return self.get_response(request)


class IntegridadeArquivosMiddleware:
    _status = None

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if getattr(settings, "MHEIBOS_INTEGRITY_ENFORCED", False):
            if IntegridadeArquivosMiddleware._status is None:
                IntegridadeArquivosMiddleware._status = check_integrity()
            ok, message = IntegridadeArquivosMiddleware._status
            if not ok:
                return HttpResponse(
                    f"Instalacao bloqueada: arquivos do programa foram alterados. {message}",
                    status=503,
                    content_type="text/plain; charset=utf-8",
                )
        return self.get_response(request)


class PrimeiroAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        caminho = request.path_info
        liberado = (
            caminho.startswith("/primeiro-admin/")
            or caminho.startswith("/licenca/")
            or caminho.startswith("/static/")
            or caminho.startswith("/media/")
            or caminho.startswith("/admin/")
        )
        if not liberado and primeiro_admin_pendente():
            return redirect("primeiro_admin")
        return self.get_response(request)


class OperadorLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        caminho = request.path_info
        liberado = (
            caminho.startswith("/login/")
            or caminho.startswith("/licenca/")
            or caminho.startswith("/sair/")
            or caminho.startswith("/producao/login/")
            or caminho.startswith("/vendas/login/")
            or caminho.startswith("/primeiro-admin/")
            or caminho.startswith("/static/")
            or caminho.startswith("/media/")
            or caminho.startswith("/admin/")
            or caminho.startswith("/api/launcher/")
        )
        if not liberado and not request.session.get("operador_nome"):
            if caminho.startswith("/producao/"):
                login_url = reverse("producao_login")
            elif caminho.startswith("/vendas/"):
                login_url = reverse("vendas_login")
            else:
                login_url = reverse("login")
            return redirect(f"{login_url}?next={request.get_full_path()}")
        return self.get_response(request)
