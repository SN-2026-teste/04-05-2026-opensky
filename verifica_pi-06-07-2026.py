# -*- coding: utf-8 -*-
"""
=============================================================================
PI 2026 — Verificação de Entrega 2
Prazo: 06/07/2026
=============================================================================
Critérios verificados:
  1.  index.html presente na branch main                          [prazo]
  2.  GitHub Pages ativo com URL pública
  3.  Branches individuais (mínimo 1 por integrante)
  4.  Commits exclusivos por branch individual
  5.  Pull Requests abertos (mínimo 1 por integrante)
  6.  Pull Requests mergeados na main
  ℹ   Trello — Kanban configurado                 [verificação manual]
  ℹ   Google Drive — pasta compartilhada          [verificação manual]
=============================================================================
Ações específicas do líder (quem criou a organização):
  - Criar página inicial base (index.html) na main
  - Ativar GitHub Pages
  - Revisar e mergear os Pull Requests dos integrantes
  - Configurar Trello (Kanban) e Google Drive
Ações de cada integrante:
  - Criar branch individual
  - Fazer commits na branch individual
  - Abrir Pull Request para a main
=============================================================================
Uso:
  python verifica_pi-06-07-2026.py
  python verifica_pi-06-07-2026.py --grupo 3
  python verifica_pi-06-07-2026.py --sem-cores > relatorio.txt
=============================================================================
"""

import subprocess, json, sys, os, argparse
from datetime import datetime

# ── Compatibilidade Windows ───────────────────────────────────────────────────
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    os.system("color")

def _suporta_cores():
    if sys.platform == "win32":
        return os.environ.get("WT_SESSION") or os.environ.get("TERM_PROGRAM")
    return sys.stdout.isatty()

_CORES = bool(_suporta_cores())
def _c(code, txt): return f"\033[{code}m{txt}\033[0m" if _CORES else txt

OK    = _c("92", "✔")
FAIL  = _c("91", "✖")
TARDE = _c("93", "⚠")
INFO  = _c("2",  "ℹ")
BOLD  = "\033[1m"  if _CORES else ""
DIM   = "\033[2m"  if _CORES else ""
RESET = "\033[0m"  if _CORES else ""
CYAN  = "\033[96m" if _CORES else ""
BLUE  = "\033[94m" if _CORES else ""
YEL   = "\033[93m" if _CORES else ""
RED   = "\033[91m" if _CORES else ""
GRN   = "\033[92m" if _CORES else ""

# ── Prazo ─────────────────────────────────────────────────────────────────────
PRAZO       = datetime(2026, 7, 6, 23, 59, 59)
PRAZO_LABEL = "06/07/2026"

# ── Grupos ────────────────────────────────────────────────────────────────────
GRUPOS = {
    1:  {"macroarea": "Cidadania e Civismo",
         "integrantes": ["Lucca Hillebrand Carraro", "Rafael Bremm Meyer", "Heitor Talarico"]},
    2:  {"macroarea": "Multiculturalismo",
         "integrantes": ["Pedro Henrique Cardoso Cavalcanti", "Gabriel Goulart Correas", "André Vilain dos Santos"]},
    3:  {"macroarea": "Ciência e Tecnologia",
         "integrantes": ["Bruno Miguel Baugart Polla", "Isaque Tehlen Souza", "Mayki Rafael Klein"]},
    4:  {"macroarea": "Saúde",
         "integrantes": ["Guilherme Rodrigues Carvalho", "Kelvin Fellipe da Silva de Souza", "Lorenzo Babeto Falkowski"]},
    5:  {"macroarea": "Cidadania e Civismo",
         "integrantes": ["Gabriel Marcos de Barros Izidoro", "Kevyn Danziger Granero Ramos", "Adryan Juliano Bieger"]},
    6:  {"macroarea": "Economia",
         "integrantes": ["Camile Vitória Blodorn", "Eduarda Valentina Tenório Caprioli", "Bruno Henrique Blodorn"]},
    7:  {"macroarea": "Ciência e Tecnologia",
         "integrantes": ["Bryan D. M. Chaves", "Nicolas da L. A. Bicudo", "Vinícius F. Caramel"]},
    8:  {"macroarea": "Multiculturalismo",
         "integrantes": ["Milena Rambo", "Fabiely Amabily", "Yasmin Reis"]},
    9:  {"macroarea": "Saúde",
         "integrantes": ["Murilo Dalla Barba Temporini", "Paolla Vithória Lucht Klauck", "Pedro Miguel Kliemann"]},
    10: {"macroarea": "Economia",
         "integrantes": ["Rafael Rossato", "Diego Nunes Ribeiro", "Eduardo Bleeper"]},
    11: {"macroarea": "Meio Ambiente",
         "integrantes": ["Heloisa Farias", "Geovana Black", "Leticia Reis"]},
    12: {"macroarea": "Meio Ambiente",
         "integrantes": ["Lucas Uhlmann", "Gabriel Senger Piana", "Pedro Geraldi"]},
}

ORG_PREFIX   = "PI-2026-Grupo"
REPO_PATTERN = "projeto-integrador-grupo{}"

# ── Infraestrutura GitHub CLI ─────────────────────────────────────────────────
def gh_api(endpoint, silent=False):
    r = subprocess.run(["gh", "api", endpoint], capture_output=True, text=True)
    if r.returncode != 0:
        return None
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return None

def get_professor_login():
    data = gh_api("/user")
    if not data:
        print(f"{RED}Erro:{RESET} execute  gh auth login  antes de rodar este script.")
        sys.exit(1)
    return data.get("login", ""), data.get("name", "")

def listar_orgs():
    data = gh_api("/user/orgs?per_page=100", silent=True)
    return [o["login"] for o in (data or [])]

def encontrar_org(num, orgs):
    p1 = f"{ORG_PREFIX}{num}".lower()
    p2 = f"{ORG_PREFIX}-{num}".lower()
    cands = [o for o in orgs
             if o.lower() == p1
             or o.lower().startswith(p1 + "-")
             or o.lower().startswith(p1 + "_")
             or o.lower() == p2
             or o.lower().startswith(p2 + "-")]
    if len(cands) == 1: return cands[0]
    if len(cands) > 1:  return cands[0]
    return None

# ── Helpers de prazo e formatação ────────────────────────────────────────────
def parse_data(iso):
    if not iso: return None
    try:    return datetime.strptime(iso.replace("Z",""), "%Y-%m-%dT%H:%M:%S")
    except: return None

def fmt_data(dt):
    return dt.strftime("%d/%m/%Y %H:%M UTC") if dt else "data indisponível"

def status_prazo(dt):
    if dt is None: return None
    return True if dt <= PRAZO else "late"

def tag_prazo(estado, dt):
    if estado == "late":
        return f"  {YEL}FORA DO PRAZO{RESET} — {fmt_data(dt)} (prazo: {PRAZO_LABEL})"
    if dt:
        return f"  {DIM}{fmt_data(dt)}{RESET}"
    return ""

def linha(estado, label, detalhe=""):
    icone = OK if estado is True else (TARDE if estado == "late" else FAIL)
    det   = f"  {DIM}{detalhe}{RESET}" if detalhe else ""
    return f"    {icone}  {label}{det}"

def linha_info(label, detalhe=""):
    det = f"  {DIM}{detalhe}{RESET}" if detalhe else ""
    return f"    {INFO}  {YEL}{label}{RESET}{det}"

def sep(c="─", n=70): print(f"{DIM}{c*n}{RESET}")

# ── Funções de verificação específicas da Entrega 2 ──────────────────────────
def checar_index_html(org, repo):
    """Verifica se index.html existe e retorna data do primeiro commit."""
    if gh_api(f"/repos/{org}/{repo}/contents/index.html", silent=True) is None:
        return False, None
    commits = gh_api(
        f"/repos/{org}/{repo}/commits?path=index.html&per_page=100",
        silent=True) or []
    if commits:
        primeiro    = commits[-1]   # lista é do mais recente ao mais antigo
        date_str    = (primeiro.get("commit", {})
                               .get("author", {})
                               .get("date"))
        return True, parse_data(date_str)
    return True, None

def checar_branches(org, repo):
    """Lista de todas as branches do repositório."""
    data = gh_api(f"/repos/{org}/{repo}/branches?per_page=100", silent=True) or []
    return [b["name"] for b in data]

def checar_commits_branch(org, repo, branch, base="main"):
    """Conta commits exclusivos de uma branch em relação à base."""
    data = gh_api(f"/repos/{org}/{repo}/compare/{base}...{branch}", silent=True)
    if not data:
        data = gh_api(f"/repos/{org}/{repo}/compare/master...{branch}", silent=True)
    if not data:
        return 0, None
    commits = data.get("commits", [])
    if commits:
        date_str = (commits[-1].get("commit", {})
                               .get("author", {})
                               .get("date"))
        return len(commits), parse_data(date_str)
    return 0, None

def checar_pull_requests(org, repo):
    """Retorna todos os PRs (abertos e fechados)."""
    return gh_api(f"/repos/{org}/{repo}/pulls?state=all&per_page=100", silent=True) or []

# ── Verificação por grupo ─────────────────────────────────────────────────────
CRITERIOS = {
    "index_html":    "index.html na main",
    "pages_ativo":   "GitHub Pages ativo",
    "branches_ind":  "Branches individuais",
    "commits_ind":   "Commits por branch",
    "prs_abertos":   "Pull Requests abertos",
    "prs_mergeados": "PRs mergeados",
}

def verificar_grupo(num, dados, orgs, professor_login):
    integrantes = dados["integrantes"]
    n_int       = len(integrantes)
    checks      = {}

    print(); sep("═")
    print(f"  {BOLD}{CYAN}GRUPO {num:02d}{RESET}  —  {dados['macroarea']}")
    print(f"  {DIM}Integrantes: {', '.join(integrantes)}{RESET}")
    sep()

    # Localizar organização e repositório
    org_login = encontrar_org(num, orgs)
    repo_nome = REPO_PATTERN.format(num)

    if not org_login:
        print(f"    {FAIL}  Organização não encontrada — entrega 2 não pode ser verificada.")
        for k in CRITERIOS:
            checks[k] = False
        return {"grupo": num, "macroarea": dados["macroarea"],
                "org_login": None, "checks": checks}

    repo_data = gh_api(f"/repos/{org_login}/{repo_nome}", silent=True)
    if not repo_data:
        print(f"    {FAIL}  Repositório '{repo_nome}' não encontrado em {org_login}.")
        for k in CRITERIOS:
            checks[k] = False
        return {"grupo": num, "macroarea": dados["macroarea"],
                "org_login": org_login, "checks": checks}

    print(f"    {DIM}Organização: {org_login}  |  Repositório: {repo_nome}{RESET}")
    sep("·")

    # 1. index.html ────────────────────────────────────────────────────────────
    tem_index, index_dt = checar_index_html(org_login, repo_nome)
    if tem_index:
        prazo_idx = status_prazo(index_dt) if index_dt else True
        detalhe   = fmt_data(index_dt) + tag_prazo(prazo_idx, index_dt) if index_dt else "presente — data indisponível"
    else:
        prazo_idx = False
        detalhe   = "arquivo não encontrado na branch main"
    checks["index_html"] = prazo_idx
    print(linha(prazo_idx, "index.html na main", detalhe))

    # 2. GitHub Pages ──────────────────────────────────────────────────────────
    pages_data = gh_api(f"/repos/{org_login}/{repo_nome}/pages", silent=True)
    pages_ok   = (pages_data is not None
                  and pages_data.get("status") in ("built", "building"))
    checks["pages_ativo"] = pages_ok
    pages_url  = (pages_data or {}).get("html_url", "")
    pages_det  = pages_url if pages_ok else "não ativado ou ainda em deploy"
    print(linha(pages_ok, "GitHub Pages ativo", pages_det))

    # 3. Branches individuais ──────────────────────────────────────────────────
    branches     = checar_branches(org_login, repo_nome)
    branches_ind = [b for b in branches if b.lower() not in ("main", "master")]
    bra_ok       = len(branches_ind) >= n_int
    checks["branches_ind"] = bra_ok
    print(linha(bra_ok,
          f"Branches individuais ({len(branches_ind)}/{n_int})",
          ", ".join(branches_ind) if branches_ind else "nenhuma além de main"))

    # 4. Commits por branch ────────────────────────────────────────────────────
    com_commits = 0
    detalhes_c  = []
    for b in branches_ind:
        n_c, ultima_dt = checar_commits_branch(org_login, repo_nome, b)
        if n_c > 0:
            com_commits += 1
            detalhes_c.append(f"{b} ({n_c} commit{'s' if n_c>1 else ''})")
        else:
            detalhes_c.append(f"{b} {RED}(sem commits exclusivos){RESET}")
    commit_ok = com_commits >= n_int
    checks["commits_ind"] = commit_ok
    print(linha(commit_ok,
          f"Commits individuais ({com_commits}/{n_int})",
          "  ".join(detalhes_c) if detalhes_c else "nenhum"))

    # 5. Pull Requests abertos ─────────────────────────────────────────────────
    prs         = checar_pull_requests(org_login, repo_nome)
    prs_merged  = [p for p in prs if p.get("merged_at")]
    prs_ok      = len(prs) >= n_int
    checks["prs_abertos"] = prs_ok
    pr_branches = [p.get("head", {}).get("ref","?") for p in prs[:6]]
    print(linha(prs_ok,
          f"Pull Requests ({len(prs)} total / {len(prs_merged)} mergeados)",
          ", ".join(pr_branches) if pr_branches else "nenhum"))

    # 6. PRs mergeados ─────────────────────────────────────────────────────────
    merge_ok = len(prs_merged) > 0
    checks["prs_mergeados"] = merge_ok
    merged_branches = [p.get("head", {}).get("ref","?") for p in prs_merged]
    print(linha(merge_ok,
          f"PRs mergeados ({len(prs_merged)})",
          ", ".join(merged_branches) if merged_branches else "nenhum mergeado ainda"))

    # ℹ Itens de verificação manual ────────────────────────────────────────────
    sep("·")
    print(linha_info("Trello", "Kanban com colunas Backlog/Em Progresso/Em Revisão/Concluído + cards — verificar manualmente"))
    print(linha_info("Google Drive", "Pasta do grupo compartilhada com integrantes e professor — verificar manualmente"))

    return {"grupo": num, "macroarea": dados["macroarea"],
            "org_login": org_login, "checks": checks}

# ── Resumo ────────────────────────────────────────────────────────────────────
def imprimir_resumo(resultados, professor_login):
    crit  = list(CRITERIOS.keys())
    curto = {
        "index_html":    "index",
        "pages_ativo":   "Pages",
        "branches_ind":  "Branch",
        "commits_ind":   "Commit",
        "prs_abertos":   "PR",
        "prs_mergeados": "Merge",
    }
    print(); sep("═", 72)
    print(f"  {BOLD}RESUMO — ENTREGA 2  (Prazo: {PRAZO_LABEL}){RESET}")
    print(f"  {DIM}Verificado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}  |  Professor: @{professor_login}{RESET}")
    print(f"  {DIM}Nota: Trello e Google Drive não são verificáveis via API — checar manualmente.{RESET}")
    sep("═", 72)

    col_g, col_c = 8, 8
    header = f"  {'Grupo':<{col_g}}" + "".join(f"{curto[c]:^{col_c}}" for c in crit) + f"  {'Total':>5}"
    print(f"{BOLD}{header}{RESET}")
    sep("─", 72)

    totais = {c: 0 for c in crit}
    ng = len(resultados)
    for r in resultados:
        ch  = r["checks"]
        ok  = sum(1 for c in crit if ch.get(c) is True)
        lt  = sum(1 for c in crit if ch.get(c) == "late")
        tot = len(crit)
        cor = GRN if ok == tot else (YEL if ok+lt >= tot-1 else RED)
        cel = ""
        for c in crit:
            v = ch.get(c, False)
            s = (f"{GRN}✔{RESET}" if v is True
                 else f"{YEL}⚠{RESET}" if v == "late"
                 else f"{RED}✖{RESET}")
            cel += f"{s:^{col_c+9}}"
        for c in crit:
            if ch.get(c) in (True, "late"): totais[c] += 1
        print(f"  {cor}Grupo {r['grupo']:02d}{RESET}  {cel}  {cor}{ok+lt}/{tot:>2}{RESET}")

    sep("─", 72)
    tot_l = "".join(
        f"{GRN if totais[c]==ng else YEL}{totais[c]}/{ng}{RESET}".center(col_c+9)
        for c in crit)
    print(f"  {'Total':<{col_g+2}}{tot_l}")
    sep("═", 72)

    pendentes = [r for r in resultados
                 if not all(r["checks"].get(c) is True for c in crit)]
    atrasados = [r for r in resultados
                 if any(r["checks"].get(c) == "late" for c in crit)]
    if pendentes:
        print(f"\n  {BOLD}{YEL}Grupos com pendências:{RESET}")
        for r in pendentes:
            ch  = r["checks"]
            aus = [CRITERIOS[c] for c in crit if not ch.get(c)]
            tar = [CRITERIOS[c] for c in crit if ch.get(c) == "late"]
            ln  = f"    {BOLD}Grupo {r['grupo']:02d}{RESET}"
            if aus: ln += f"  {RED}Ausente:{RESET} {', '.join(aus)}"
            if tar: ln += f"  {YEL}Fora do prazo:{RESET} {', '.join(tar)}"
            print(ln)
    else:
        print(f"\n  {GRN}{BOLD}Todos os grupos em conformidade com a Entrega 2.{RESET}")
    if atrasados:
        print(f"\n  {BOLD}Legenda:{RESET} {OK} no prazo  {TARDE} fora do prazo ({PRAZO_LABEL})  {FAIL} não entregue  {INFO} verificação manual")
    print()

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(
        description=f"PI 2026 — Entrega 2 — Prazo {PRAZO_LABEL}")
    ap.add_argument("--grupo", type=int, default=None,
        help="Verificar apenas o grupo N. Padrão: todos.")
    ap.add_argument("--sem-cores", action="store_true",
        help="Desativar cores ANSI.")
    args = ap.parse_args()

    if args.sem_cores:
        global OK,FAIL,TARDE,INFO,BOLD,DIM,RESET,CYAN,BLUE,YEL,RED,GRN,_CORES
        _CORES=False
        OK="OK"; FAIL="XX"; TARDE="[ATRASO]"; INFO="i"
        BOLD=DIM=RESET=CYAN=BLUE=YEL=RED=GRN=""

    print(); sep("═",72)
    print(f"  {BOLD}PI 2026 — Verificação Entrega 2  |  Prazo: {PRAZO_LABEL}{RESET}")
    print(f"  {DIM}verifica_pi-06-07-2026.py  |  {datetime.now().strftime('%d/%m/%Y %H:%M')}{RESET}")
    sep("═",72)

    print(f"\n  Detectando usuário autenticado...")
    prof_login, prof_nome = get_professor_login()
    print(f"  {OK}  @{prof_login}  ({prof_nome})")

    print(f"\n  Carregando organizações...")
    orgs    = listar_orgs()
    orgs_pi = [o for o in orgs if "PI-2026" in o.upper()]
    print(f"  {OK}  {len(orgs)} org(s) total  |  {len(orgs_pi)} com prefixo PI-2026")
    if orgs_pi:
        print(f"  {DIM}  {', '.join(orgs_pi)}{RESET}")

    grupos_alvo = {args.grupo: GRUPOS[args.grupo]} if args.grupo else GRUPOS
    resultados  = []
    for num, dados in sorted(grupos_alvo.items()):
        resultados.append(verificar_grupo(num, dados, orgs, prof_login))

    if len(resultados) > 1:
        imprimir_resumo(resultados, prof_login)
    else:
        r  = resultados[0]
        ok = sum(1 for v in r["checks"].values() if v in (True, "late"))
        print(f"\n  Grupo {args.grupo} — {ok}/{len(r['checks'])} critérios concluídos\n")

if __name__ == "__main__":
    main()
