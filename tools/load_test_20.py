import argparse
import statistics
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from html.parser import HTMLParser
from http.cookiejar import CookieJar


DEFAULT_PATHS = [
    "/",
    "/pedidos/",
    "/pedidos/novo/",
    "/pedidos/?status=EM_PRODUCAO",
    "/pedidos/?status=PRONTO",
    "/pedidos/entrega/",
    "/producao/",
    "/produtos/",
    "/assistencia-envio/",
    "/dashboard/",
    "/dashboard/?aba=relatorios",
    "/dashboard/?aba=crm",
    "/configuracoes/?aba=usuarios",
    "/api/widgets/prazos/",
    "/api/notificacoes/assistencia/",
]


class CsrfParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.token = ""

    def handle_starttag(self, tag, attrs):
        if tag != "input":
            return
        data = dict(attrs)
        if data.get("name") == "csrfmiddlewaretoken":
            self.token = data.get("value", "")


@dataclass
class Result:
    worker: int
    path: str
    status: int
    seconds: float
    ok: bool
    error: str = ""


def build_opener():
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(CookieJar()))


def fetch(opener, url, data=None, timeout=20, headers=None):
    encoded = None
    if data is not None:
        encoded = urllib.parse.urlencode(data).encode("utf-8")
    request = urllib.request.Request(url, data=encoded, headers=headers or {})
    started = time.perf_counter()
    try:
        with opener.open(request, timeout=timeout) as response:
            body = response.read()
            return response.getcode(), body, time.perf_counter() - started, ""
    except urllib.error.HTTPError as exc:
        body = exc.read()
        return exc.code, body, time.perf_counter() - started, str(exc)
    except Exception as exc:
        return 0, b"", time.perf_counter() - started, repr(exc)


def login(base_url, usuario, senha):
    opener = build_opener()
    status, body, _, error = fetch(opener, f"{base_url}/login/")
    if status != 200:
        raise RuntimeError(f"Falha ao abrir login: HTTP {status} {error}")
    parser = CsrfParser()
    parser.feed(body.decode("utf-8", errors="ignore"))
    if not parser.token:
        raise RuntimeError("Token CSRF nao encontrado na tela de login.")
    headers = {"Referer": f"{base_url}/login/"}
    status, body, _, error = fetch(
        opener,
        f"{base_url}/login/",
        data={"csrfmiddlewaretoken": parser.token, "usuario": usuario, "senha": senha, "next": "/"},
        headers=headers,
    )
    if status not in {200, 302}:
        raise RuntimeError(f"Falha no login: HTTP {status} {error}")
    return opener


def worker(worker_id, base_url, usuario, senha, paths, rounds):
    started = time.perf_counter()
    try:
        opener = login(base_url, usuario, senha)
    except Exception as exc:
        return [Result(worker_id, "/login/", 0, time.perf_counter() - started, False, repr(exc))]
    return navegar(worker_id, opener, base_url, paths, rounds)


def navegar(worker_id, opener, base_url, paths, rounds):
    results = []
    for _ in range(rounds):
        for path in paths:
            url = f"{base_url}{path}"
            status, body, seconds, error = fetch(opener, url)
            text = body[:600].decode("utf-8", errors="ignore")
            redirected_to_login = status == 200 and "Acesse o sistema administrativo" in text and path != "/login/"
            ok = 200 <= status < 400 and not redirected_to_login
            if redirected_to_login:
                error = "redirecionou para login"
            results.append(Result(worker_id, path, status, seconds, ok, error))
    return results


def percentile(values, percent):
    if not values:
        return 0
    ordered = sorted(values)
    index = min(len(ordered) - 1, round((percent / 100) * (len(ordered) - 1)))
    return ordered[index]


def main():
    parser = argparse.ArgumentParser(description="Teste simples de 20 acessos simultaneos no Mheibos Gestor.")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--users", type=int, default=20)
    parser.add_argument("--rounds", type=int, default=2)
    parser.add_argument("--usuario", default="Alexandre")
    parser.add_argument("--senha", default="1234")
    parser.add_argument("--prelogin", action="store_true", help="Faz login antes e mede apenas a navegacao simultanea.")
    args = parser.parse_args()

    base_url = args.base_url.rstrip("/")
    started = time.perf_counter()
    all_results = []
    if args.prelogin:
        openers = []
        for i in range(args.users):
            login_started = time.perf_counter()
            try:
                openers.append((i + 1, login(base_url, args.usuario, args.senha)))
            except Exception as exc:
                all_results.append(Result(i + 1, "/login/", 0, time.perf_counter() - login_started, False, repr(exc)))
        started = time.perf_counter()
        with ThreadPoolExecutor(max_workers=max(len(openers), 1)) as executor:
            futures = [
                executor.submit(navegar, worker_id, opener, base_url, DEFAULT_PATHS, args.rounds)
                for worker_id, opener in openers
            ]
            for future in as_completed(futures):
                all_results.extend(future.result())
    else:
        with ThreadPoolExecutor(max_workers=args.users) as executor:
            futures = [
                executor.submit(worker, i + 1, base_url, args.usuario, args.senha, DEFAULT_PATHS, args.rounds)
                for i in range(args.users)
            ]
            for future in as_completed(futures):
                all_results.extend(future.result())

    elapsed = time.perf_counter() - started
    failures = [item for item in all_results if not item.ok]
    timings = [item.seconds for item in all_results if item.ok]
    by_path = {}
    for item in all_results:
        by_path.setdefault(item.path, []).append(item)

    print(f"Base URL: {base_url}")
    print(f"Usuarios simultaneos: {args.users}")
    print(f"Rodadas por usuario: {args.rounds}")
    print(f"Requisicoes totais: {len(all_results)}")
    print(f"Tempo total: {elapsed:.2f}s")
    print(f"Falhas: {len(failures)}")
    if timings:
        print(f"Tempo medio: {statistics.mean(timings):.3f}s")
        print(f"P95: {percentile(timings, 95):.3f}s")
        print(f"P99: {percentile(timings, 99):.3f}s")

    print("\nPor pagina:")
    for path, items in sorted(by_path.items()):
        path_timings = [item.seconds for item in items if item.ok]
        path_failures = [item for item in items if not item.ok]
        avg = statistics.mean(path_timings) if path_timings else 0
        p95 = percentile(path_timings, 95)
        print(f"- {path}: {len(items) - len(path_failures)}/{len(items)} ok, media {avg:.3f}s, p95 {p95:.3f}s")

    if failures:
        print("\nFalhas encontradas:")
        for item in failures[:30]:
            print(f"- usuario {item.worker} {item.path}: HTTP {item.status} em {item.seconds:.3f}s {item.error}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
