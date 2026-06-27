"""Widget flutuante do Gestor — sobrepõe qualquer janela do Windows (fora do navegador)."""

from __future__ import annotations

import json
import sys
import threading
import tkinter as tk
import urllib.error
import urllib.parse
import urllib.request
from typing import Callable

BASE_URL = "http://127.0.0.1:8000"
THUMB_SIZE = 42
MAX_ITENS = 9
INTERVALO_PADRAO_MS = 30 * 60 * 1000
VISIVEL_PADRAO_MS = 60 * 1000


def _get_json(path):
    with urllib.request.urlopen(f"{BASE_URL}{path}", timeout=8) as response:
        return json.loads(response.read().decode("utf-8"))


def _carregar_prefs():
    try:
        return _get_json("/api/preferencias/")
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError):
        return {"widgets": {"prazos": {"ativo": True, "modo": "sempre", "categorias": []}}}


def _carregar_pedidos(categorias):
    query = ""
    if categorias:
        query = "?" + urllib.parse.urlencode({"categorias": ",".join(str(c) for c in categorias)})
    try:
        dados = _get_json(f"/api/widgets/prazos/{query}")
        return dados.get("pedidos", [])
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError):
        return []


class WidgetOverlayWindows:
    def __init__(self, ao_clicar: Callable[[dict], None] | None = None):
        self.ao_clicar = ao_clicar
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.95)
        self.root.configure(bg="#151823")
        self._fotos = []
        self._timer_sumir = None
        self._timer_loop = None
        self._largura = 120

    def iniciar(self):
        prefs = _carregar_prefs()
        if not prefs.get("widgets", {}).get("prazos", {}).get("ativo", True):
            return
        self.root.after(1200, self._ciclo)
        self.root.mainloop()

    def _limpar(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self._fotos.clear()

    def _ciclo(self):
        prefs = _carregar_prefs()
        conf = prefs.get("widgets", {}).get("prazos", {})
        if not conf.get("ativo", True):
            self._agendar_proximo(conf)
            return
        pedidos = _carregar_pedidos(conf.get("categorias") or [])
        if not pedidos and conf.get("modo") != "sempre":
            self._agendar_proximo(conf)
            return
        self._montar(pedidos, conf)
        self._posicionar()
        self.root.deiconify()
        self.root.lift()
        self.root.attributes("-topmost", True)
        if conf.get("modo") == "sempre":
            self._agendar_proximo(conf, 60 * 1000)
            return
        visivel = int(conf.get("visivel_segundos") or 60) * 1000
        if self._timer_sumir:
            self.root.after_cancel(self._timer_sumir)
        self._timer_sumir = self.root.after(visivel, self._ocultar)

    def _montar(self, pedidos, conf):
        self._limpar()
        frame = tk.Frame(self.root, bg="#151823", highlightbackground="#3d4275", highlightthickness=1)
        frame.pack(padx=6, pady=6)

        if not pedidos:
            tk.Label(
                frame,
                text="Nenhum prazo urgente",
                bg="#151823",
                fg="#d8ddf5",
                font=("Segoe UI", 9),
            ).pack(side="left", padx=8, pady=8)
            self._largura = 180
            btn = tk.Button(frame, text="×", command=self._ocultar, bg="#242a3f", fg="white", bd=0, width=2)
            btn.pack(side="right", padx=4, pady=4)
            return

        for pedido in pedidos[:MAX_ITENS]:
            item = tk.Frame(frame, bg="#151823")
            item.pack(side="left", padx=4)

            def abrir(p=pedido):
                self._ocultar()
                if self.ao_clicar:
                    self.ao_clicar(p)
                else:
                    import webbrowser

                    webbrowser.open(f"{BASE_URL}{p.get('url', '/')}")

            btn = tk.Button(
                item,
                text=(pedido.get("categoria_curta") or "Arte")[:8],
                width=5,
                height=2,
                bg="#3e445c",
                fg="white",
                bd=0,
                command=abrir,
            )
            btn.pack()
            tk.Label(
                item,
                text=(pedido.get("cliente") or "")[:10],
                bg="#151823",
                fg="#9aa7d3",
                font=("Segoe UI", 7),
            ).pack()

        fechar = tk.Button(frame, text="×", command=self._ocultar, bg="#242a3f", fg="white", bd=0, width=2)
        fechar.pack(side="right", padx=4, pady=4)
        self._largura = max(160, 56 + len(pedidos[:MAX_ITENS]) * 58)

    def _posicionar(self):
        self.root.update_idletasks()
        largura = self._largura
        altura = 78
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w - largura) // 2
        y = screen_h - altura - 56
        self.root.geometry(f"{largura}x{altura}+{x}+{y}")

    def _ocultar(self):
        if self._timer_sumir:
            self.root.after_cancel(self._timer_sumir)
            self._timer_sumir = None
        self.root.withdraw()
        prefs = _carregar_prefs()
        conf = prefs.get("widgets", {}).get("prazos", {})
        self._agendar_proximo(conf)

    def _agendar_proximo(self, conf, atraso_ms=None):
        if self._timer_loop:
            self.root.after_cancel(self._timer_loop)
        if atraso_ms is None:
            minutos = int(conf.get("intervalo_minutos") or 30)
            atraso_ms = max(60, minutos) * 60 * 1000
        self._timer_loop = self.root.after(atraso_ms, self._ciclo)


def main():
    if len(sys.argv) > 1:
        global BASE_URL
        BASE_URL = sys.argv[1].rstrip("/")
    WidgetOverlayWindows().iniciar()


if __name__ == "__main__":
    main()
