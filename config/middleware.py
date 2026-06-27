from django.shortcuts import redirect
from django.urls import reverse

from apps.catalogo.bootstrap import primeiro_admin_pendente


class PrimeiroAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        caminho = request.path_info
        liberado = (
            caminho.startswith("/primeiro-admin/")
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
            or caminho.startswith("/sair/")
            or caminho.startswith("/producao/login/")
            or caminho.startswith("/primeiro-admin/")
            or caminho.startswith("/static/")
            or caminho.startswith("/media/")
            or caminho.startswith("/admin/")
            or caminho.startswith("/api/launcher/")
        )
        if not liberado and not request.session.get("operador_nome"):
            login_url = reverse("producao_login") if caminho.startswith("/producao/") else reverse("login")
            return redirect(f"{login_url}?next={request.get_full_path()}")
        return self.get_response(request)
