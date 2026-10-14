# Manual do EX3 — Redis

## 1. Pré-requisitos
- Python 3 e o ambiente virtual do projeto (`.venv`) ativado.
- Uma instância de Redis (Redis Cloud gratuito) e o banco `mercadolivre_ex2` no MongoDB, com usuários que
  tenham os campos `email`, `favoritos` (lista de `ObjectId` de produtos) e `end` (lista de endereços
  com `logradouro`, `num`, `bairro`, `cidade`, `estado`, `cep`).

## 2. Instalação
```bash
pip install -r requirements.txt     # inclui redis, python-dotenv e pymongo
cp .env.example .env                # preencha MONGO_URI e as credenciais do Redis
```
O `.env` nunca deve ser enviado ao Git.

## 3. Como executar
Na pasta raiz do projeto, com o `.venv` ativo:
```bash
python menu.py
```
O sistema sempre pede login ao abrir. Usuário e senha aparecem na tela como "colinha"
(`admin` / `admin123`); para esconder, use `LOGIN_MOSTRAR_DICA=false`.

## 4. Menu
| Opção | Função |
|---|---|
| 1 a 4 | CRUD de Usuário, Vendedor, Produto e Compra (EX2) |
| 5 | Mongo → Redis: copia favoritos e endereços de cada usuário para o Redis |
| 6 | Redis → Mongo: devolve ao Mongo os itens (já editados) |
| 7 | CRUD no Redis: Create, Read, Update, Delete de favoritos e endereços |
| S | Sair (encerra a sessão no Redis) |

## 5. Fluxo do exercício
1. Opção **5**: envia os itens ao Redis.
2. Opção **7**: altera os itens (criar, ler, atualizar, apagar). O usuário é escolhido por nome, CPF ou e-mail.
3. Opção **6**: devolve ao Mongo. Confira no Mongo (Compass/Atlas) ou no Redis Insight.

## 6. Sessão e tempo de expiração
- A sessão é a chave `sessao:ativa` no Redis, criada no login com `SET` + `EXPIRE`.
- Todo menu verifica a sessão e imprime `[Sessão] verificada em '<menu>': OK | usuário | expira em Ns`.
- Ao expirar, aparece o aviso, o sistema faz logout e a tela de login surge sozinha após
  `SESSAO_ESPERA_LOGIN` segundos (o que estava sendo digitado é descartado).
- Para a apresentação use `SESSAO_TTL=7`; para uso normal, `SESSAO_TTL=1800`. Basta editar o `.env`.

| Variável | Padrão | Significado |
|---|---|---|
| `SESSAO_TTL` | 1800 | Segundos de vida da sessão |
| `SESSAO_RENOVAR` | false | `true` renova o tempo a cada acesso a menu |
| `SESSAO_ESPERA_LOGIN` | 2 | Segundos entre o aviso e a tela de login |
| `SESSAO_LOGOUT_AUTO` | true | `false` só percebe a expiração ao abrir um menu |
| `LOGIN_MOSTRAR_DICA` | true | Mostra a colinha de login |

## 7. Como testar
Os casos estão em `docs/testes.md` (EX3-01 a EX3-50), com passos e resultado esperado.
Roteiro rápido: (1) login; (2) opção 5 e conferir as chaves no Redis Insight; (3) opção 7, alterar a
cidade de um endereço; (4) opção 6 e conferir no Mongo; (5) `SESSAO_TTL=7` para ver a expiração.

## 8. Problemas comuns
| Sintoma | Causa e solução |
|---|---|
| `ModuleNotFoundError: app` | Terminal fora da pasta raiz do projeto |
| `invalid username-password pair` | Senha do Redis diferente da do `.env` (confira se salvou a mudança no Redis Cloud) |
| `getaddrinfo failed` | `REDIS_HOST` com `@` ou espaço sobrando |
| Tempo da sessão não muda | Salvar o `.env`; apagar a chave `sessao:ativa` antiga |
| Login pede ENTER após expirar | O terminal não é um console de verdade; use o terminal do VS Code ou o cmd |