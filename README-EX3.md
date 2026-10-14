## EX3 — Redis (BDNR)

Etapa construída sobre o app do EX2 (marketplace estilo Mercado Livre em Python + MongoDB), na branch `redis`.

### O que foi feito
1. **Mongo → Redis (opção 5):** copia os **favoritos** e os **endereços** de cada usuário para o Redis
   (`fav_<email>` e `end_<email>`, listas em JSON). O Mongo não perde nada.
2. **CRUD no Redis (opção 7):** Create, Read, Update e Delete dos favoritos e endereços direto no Redis,
   escolhendo o usuário por nome, CPF ou e-mail.
3. **Redis → Mongo (opção 6):** devolve ao Mongo os itens editados (favoritos voltam como `ObjectId`).
4. **Autenticação com sessão temporária:** login fixo no código; a sessão fica na chave `sessao:ativa`
   do Redis com tempo de vida definido pelo comando `EXPIRE`. Todo acesso a menu verifica a sessão e
   mostra `[Sessão] verificada em '<menu>'`. Ao expirar: aviso, logout e volta sozinho para o login.

### Arquivos
| Arquivo | Função |
|---|---|
| `app/redis_sessao.py` | Conexão Redis, login/sessão com `expire`, sincronização Mongo ⇄ Redis |
| `app/redis_crud.py` | CRUD dos itens no Redis (opção 7) |
| `menu.py` | Menu principal com as opções 5, 6 e 7 e a verificação de sessão |
| `.env.example` | Modelo das variáveis de configuração |
| `docs/testes.md` | Casos de teste do EX3 (EX3-01 a EX3-50) |

### Configuração
Copie `.env.example` para `.env` e preencha (o `.env` está no `.gitignore`).
Para a apresentação, use `SESSAO_TTL=7`; para uso normal, `SESSAO_TTL=1800`.

Manual completo: `docs/manual-ex3.md`.