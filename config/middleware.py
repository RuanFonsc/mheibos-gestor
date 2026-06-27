from django.shortcuts import redirect

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
