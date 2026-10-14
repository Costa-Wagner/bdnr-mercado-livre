"""EX3 - Redis: sincronização Mongo <-> Redis e sessão de login com expiração.

Colocar em app/redis_sessao.py.  pip install redis python-dotenv

Configuração por variáveis de ambiente (arquivo .env, que fica no .gitignore):
    REDIS_HOST, REDIS_PORT, REDIS_USERNAME, REDIS_PASSWORD
    SESSAO_TTL       tempo da sessão em segundos
                     apresentação: SESSAO_TTL=7
                     uso normal  : SESSAO_TTL=1800   (30 min, padrão se omitido)
    SESSAO_RENOVAR   "true" renova o TTL a cada acesso ao menu (padrão: false)
    SESSAO_LOGOUT_AUTO    "true" avisa na tela e faz logout na hora ao expirar; o próximo
                          acesso exige novo login (padrão: true). O programa NÃO fecha.
    SESSAO_ESPERA_LOGIN   segundos entre o aviso de expiração e a tela de login (padrão: 3)
    LOGIN_MOSTRAR_DICA    "true" mostra a colinha usuário/senha no login (padrão: true)
"""
import hashlib
import json
import os
import sys
import threading
import time
import uuid
import builtins
from getpass import getpass
from pathlib import Path

import redis
from bson import ObjectId
from dotenv import load_dotenv

from app.conexao import db  # ajuste se o nome exportado for outro

# Sempre lê o .env da RAIZ do projeto (pasta acima de app/) e faz o .env mandar
# nas variáveis de ambiente já existentes (override), para o TTL valer o que está no arquivo.
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(ENV_PATH, override=True)

# ------------------------------------------------------------------ config
COLECAO = db.usuario                      # coleção de usuários do EX2
CAMPO_EMAIL = "email"
CAMPO_FAVORITOS = "favoritos"             # lista de ObjectId (produtos)
CAMPO_ENDERECOS = "end"                   # lista de {logradouro, num, bairro, cidade, estado, cep}

SESSAO_TTL = int(os.getenv("SESSAO_TTL", 1800))
SESSAO_RENOVAR = os.getenv("SESSAO_RENOVAR", "false").lower() == "true"
SESSAO_KEY = "sessao:ativa"
# true  = ao expirar, faz logout na hora (aviso na tela) e o próximo acesso exige novo login
# false = só percebe a expiração no próximo acesso a um menu
SESSAO_LOGOUT_AUTO = os.getenv("SESSAO_LOGOUT_AUTO", "true").lower() == "true"
SESSAO_ESPERA_LOGIN = float(os.getenv("SESSAO_ESPERA_LOGIN", 3))
_vigia_ativo = False
_expirou = threading.Event()

# Login hardcoded (senha guardada como hash sha256, igual ao resto do projeto)
LOGIN_USER = "admin"
LOGIN_SENHA = "admin123"
LOGIN_SENHA_HASH = hashlib.sha256(LOGIN_SENHA.encode()).hexdigest()

# "Colinha" na tela de login (apresentação). Para esconder: LOGIN_MOSTRAR_DICA=false no .env
LOGIN_MOSTRAR_DICA = os.getenv("LOGIN_MOSTRAR_DICA", "true").lower() == "true"
LOGIN_USER_DICA = LOGIN_USER
LOGIN_SENHA_DICA = LOGIN_SENHA

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    username=os.getenv("REDIS_USERNAME") or "default",
    password=os.getenv("REDIS_PASSWORD") or None,
    decode_responses=True,
)


# ------------------------------------------------------------------ sessão
def _vigiar_sessao():
    """Thread de fundo: dorme até a chave expirar, avisa na tela e marca o logout.
    Se a sessão for renovada (SESSAO_RENOVAR), o PTTL volta a subir e ela continua vigiando.
    O programa não fecha: o próximo acesso a um menu exige novo login."""
    global _vigia_ativo
    while True:
        restante_ms = r.pttl(SESSAO_KEY)
        if restante_ms < 0:          # -2 = chave não existe mais (expirou)
            break
        time.sleep(restante_ms / 1000 + 0.2)
    _expirou.set()
    _vigia_ativo = False
    print("\n\n[Sessão] EXPIRADA: logout realizado. Redirecionando para o login...")
    sys.stdout.flush()


def _iniciar_vigia():
    """Liga o vigia (uma vez por sessão): no login OU ao reaproveitar uma sessão válida."""
    global _vigia_ativo
    if SESSAO_LOGOUT_AUTO and not _vigia_ativo:
        _vigia_ativo = True
        threading.Thread(target=_vigiar_sessao, daemon=True).start()


def _gravar_sessao(usuario):
    """Grava a sessão no Redis e usa a função EXPIRE para definir o tempo de vida."""
    dados = json.dumps({"usuario": usuario, "token": str(uuid.uuid4())})
    pipe = r.pipeline()              # MULTI/EXEC: set + expire de uma vez, sem brecha entre eles
    pipe.set(SESSAO_KEY, dados)
    pipe.expire(SESSAO_KEY, SESSAO_TTL)
    pipe.execute()
    _expirou.clear()
    _iniciar_vigia()


def encerrar_sessao():
    """Logout: apaga a sessão no Redis."""
    r.delete(SESSAO_KEY)


def sessao_expirou():
    """True (uma única vez) se a sessão expirou enquanto o programa esperava uma digitação.
    Quem chama descarta o que foi digitado e volta ao início do menu, que exige novo login."""
    if _expirou.is_set():
        _expirou.clear()
        return True
    return False


def _tem_terminal():
    try:
        return sys.stdin.isatty()
    except Exception:
        return False


def _ler_linha_ate_expirar(msg):
    """Lê uma linha do teclado, mas desiste (retorna None) se a sessão expirar enquanto espera.
    Fica checando o teclado a cada instante em vez de travar no input()."""
    print(msg, end="", flush=True)
    if os.name == "nt":                      # Windows: lê tecla a tecla
        import msvcrt
        buf = []
        while not _expirou.is_set():
            if not msvcrt.kbhit():
                time.sleep(0.05)
                continue
            ch = msvcrt.getwch()
            if ch in ("\r", "\n"):
                print()
                return "".join(buf)
            if ch == "\x03":                 # Ctrl+C
                raise KeyboardInterrupt
            if ch in ("\x00", "\xe0"):       # tecla especial (setas, F1...): descarta o código seguinte
                msvcrt.getwch()
            elif ch == "\b":                 # backspace
                if buf:
                    buf.pop()
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
            else:
                buf.append(ch)
                sys.stdout.write(ch)
                sys.stdout.flush()
        return None
    import select                            # Linux/Mac
    while not _expirou.is_set():
        pronto, _, _ = select.select([sys.stdin], [], [], 0.1)
        if pronto:
            linha = sys.stdin.readline()
            if linha == "":
                raise EOFError
            return linha.rstrip("\n")
    return None


def ler_opcao(msg):
    """Como input().strip().upper() para as opções dos menus, mas, se a sessão expirar enquanto
    espera a digitação, avisa, espera SESSAO_ESPERA_LOGIN segundos e retorna None: o menu então
    volta sozinho para a tela de login. Sem terminal interativo, usa o input() normal."""
    if not (SESSAO_LOGOUT_AUTO and _tem_terminal()):
        return input(msg).strip().upper()
    texto = _ler_linha_ate_expirar(msg)
    if texto is None:
        _expirou.clear()
        time.sleep(SESSAO_ESPERA_LOGIN)
        return None
    return texto.strip().upper()

def _ler_senha_mascarada(msg):
    """Lê a senha mostrando um * por tecla digitada. Sem terminal interativo, usa o getpass."""
    if not _tem_terminal():
        return getpass(msg)
    print(msg, end="", flush=True)
    buf = []
    if os.name == "nt":                      # Windows
        import msvcrt
        while True:
            ch = msvcrt.getwch()
            if ch in ("\r", "\n"):
                print()
                return "".join(buf)
            if ch == "\x03":                 # Ctrl+C
                raise KeyboardInterrupt
            if ch in ("\x00", "\xe0"):       # tecla especial: descarta o código seguinte
                msvcrt.getwch()
            elif ch == "\b":                 # backspace
                if buf:
                    buf.pop()
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
            else:
                buf.append(ch)
                sys.stdout.write("*")
                sys.stdout.flush()
    import termios, tty                      # Linux/Mac
    fd = sys.stdin.fileno()
    antigo = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        while True:
            ch = sys.stdin.read(1)
            if ch in ("\r", "\n"):
                print()
                return "".join(buf)
            if ch in ("\x7f", "\b"):
                if buf:
                    buf.pop()
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
            else:
                buf.append(ch)
                sys.stdout.write("*")
                sys.stdout.flush()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, antigo)

def login():
    """Pede usuário/senha (hardcoded) e abre a sessão no Redis com TTL."""
    print(f"\n=== Login (sessão de {SESSAO_TTL}s) ===")
    if LOGIN_MOSTRAR_DICA:
        print(f"[hardcoded] usuário: {LOGIN_USER_DICA} | senha: {LOGIN_SENHA_DICA}")
    user = input("Usuário: ").strip()
    senha = _ler_senha_mascarada("Senha: ")
    if user == LOGIN_USER and hashlib.sha256(senha.encode()).hexdigest() == LOGIN_SENHA_HASH:
        _gravar_sessao(user)
        print("Login realizado.")
        return True
    print("Usuário ou senha inválidos.")
    return False


def ler_sim_nao(msg):
    """Pergunta S/N (maiúscula ou minúscula). Só aceita S ou N; senão pergunta de novo.
    Retorna True para S e False para N."""
    while True:
        resp = input(msg).strip().upper()
        if resp in ("S", "N"):
            return resp == "S"
        print("Opção inválida. Digite S ou N.")


def sessao_valida(menu="Menu principal"):
    """Verifica a sessão no Redis e mostra na tela que a verificação foi feita,
    informando em qual menu. Retorna True se há sessão ativa."""
    dados = r.get(SESSAO_KEY)
    if not dados:
        print(f"\n[Sessão] verificação em '{menu}': EXPIRADA ou inexistente.")
        return False
    if SESSAO_RENOVAR:
        r.expire(SESSAO_KEY, SESSAO_TTL)
    usuario = json.loads(dados)["usuario"]
    print(f"\n[Sessão] verificada em '{menu}': OK | usuário: {usuario} | expira em {r.ttl(SESSAO_KEY)}s")
    _iniciar_vigia()   # sessão aproveitada de uma execução anterior também precisa ser vigiada
    return True


def exigir_sessao(menu="Menu principal"):
    """Chamar em TODO acesso a menu. Garante sessão válida; se expirou, força novo login.
    Retorna False quando a pessoa desiste (responde N) e o app deve encerrar."""
    while not sessao_valida(menu):
        if not login():
            if not ler_sim_nao("Tentar de novo (S/N)? "):
                return False
    return True


# ------------------------------------------------------------------ sync
def mongo_para_redis():
    """Opção 5: Favoritos e Endereços de cada usuário (Mongo) -> Redis."""
    total = 0
    for u in COLECAO.find({CAMPO_EMAIL: {"$exists": True}}):
        email = u[CAMPO_EMAIL]
        favs = [str(f) for f in u.get(CAMPO_FAVORITOS, [])]   # ObjectId -> str
        ends = u.get(CAMPO_ENDERECOS, [])
        r.set(f"fav_{email}", json.dumps(favs))
        r.set(f"end_{email}", json.dumps(ends, ensure_ascii=False))
        print(f"fav_{email}  |  end_{email}")
        total += 1
    print(f"{total} usuário(s) enviados ao Redis.")


def redis_para_mongo():
    """Opção 6: lê fav_*/end_* (já editados no Redis) e grava no Mongo."""
    atualizados = 0
    for prefixo, campo in (("fav_", CAMPO_FAVORITOS), ("end_", CAMPO_ENDERECOS)):
        for chave in r.scan_iter(f"{prefixo}*"):
            email = chave[len(prefixo):]
            try:
                valor = json.loads(r.get(chave))
                if campo == CAMPO_FAVORITOS:
                    valor = [ObjectId(f) for f in valor]      # str -> ObjectId
            except Exception:
                print(f"Ignorando {chave}: conteúdo inválido.")
                continue
            res = COLECAO.update_one({CAMPO_EMAIL: email}, {"$set": {campo: valor}})
            if res.matched_count:
                print(f"{chave} -> Mongo ({campo})")
                atualizados += 1
            else:
                print(f"{chave}: usuário não encontrado no Mongo.")
    print(f"{atualizados} campo(s) atualizados no Mongo.")

_input_original = builtins.input

class SessaoExpirada(BaseException):
    """A sessão expirou enquanto o programa esperava uma digitação."""

def _input_vigiado(msg=""):
    """Substitui o input() do programa inteiro: com sessão ativa, desiste da digitação
    assim que ela expira e levanta SessaoExpirada (nada do formulário é gravado)."""
    if SESSAO_LOGOUT_AUTO and _vigia_ativo and _tem_terminal():
        texto = _ler_linha_ate_expirar(msg)
        if texto is None:
            _expirou.clear()
            raise SessaoExpirada
        return texto
    return _input_original(msg)


builtins.input = _input_vigiado