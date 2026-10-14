## EX3 — Redis (sincronização Mongo ⇄ Redis, CRUD no Redis e sessão)

Pré-requisitos: Redis acessível, `.env` preenchido, ao menos 1 usuário no Mongo com `email`, `favoritos` (lista de ObjectId de produtos) e `end` (lista de endereços).
Para a demonstração da sessão use `SESSAO_TTL=7`; para os testes de sincronização e CRUD use `SESSAO_TTL=120`; para uso normal, `1800`.
Login hardcoded: `admin` / `admin123` (a "colinha" aparece na tela de login; `LOGIN_MOSTRAR_DICA=false` esconde).
O programa sempre pede login ao abrir. Ao expirar, o sistema faz logout (sem fechar o programa) e exige novo login (`SESSAO_LOGOUT_AUTO=true`, padrão).

### Sessão

| ID | Caso de teste | Passos | Resultado esperado | Status |
|----|---------------|--------|--------------------|--------|
| EX3-01 | Login sempre exigido ao abrir | Logar, sair com `S`, abrir de novo | Pede login novamente (a sessão anterior foi encerrada) | OK |
| EX3-02 | Login válido | Digitar `admin` / `admin123` | "Login realizado."; `[Sessão] verificada em 'Menu principal': OK` com usuário e tempo restante | OK |
| EX3-03 | Colinha na tela de login | Abrir o app | Aparece `[colinha] usuário: admin \| senha: admin123` | OK |
| EX3-04 | Login inválido | Informar usuário ou senha errados | "Usuário ou senha inválidos."; pergunta `Tentar de novo (S/N)?`; menu não é exibido | OK |
| EX3-05 | S/N aceita maiúscula e minúscula | Após login inválido, responder `s`; errar de novo e responder `N` | `s`/`S` tentam de novo; `n`/`N` encerram o app | OK |
| EX3-06 | S/N rejeita outras respostas | Após login inválido, responder `x`, `sim` ou Enter | "Opção inválida. Digite S ou N."; a pergunta se repete | OK |
| EX3-07 | Verificação em cada menu | Com sessão válida, abrir os menus 1 a 7 | Cada acesso mostra `[Sessão] verificada em '<nome do menu>': OK` | OK |
| EX3-08 | Contagem regressiva do TTL | Fazer login; abrir dois menus com alguns segundos de intervalo | O valor `expira em Ns` diminui entre as verificações | OK |
| EX3-09 | Expiração faz logout automático | `SESSAO_TTL=7`; login; ficar parado mais de 7s | Aparece `[Sessão] EXPIRADA: logout realizado. Redirecionando para o login...`; após `SESSAO_ESPERA_LOGIN` segundos (3) a tela de login aparece sozinha, sem ENTER; o programa não fecha | OK |
| EX3-10 | Novo login exigido após expirar | Após EX3-09, apenas aguardar (sem digitar) | Aparece `verificação em 'Menu principal': EXPIRADA` e a tela de login automaticamente | OK |
| EX3-11 | Opção digitada após expirar é descartada | Login; esperar expirar; digitar `1` sem dar ENTER | O texto digitado é descartado; vai para o login; após logar volta ao menu principal | OK |
| EX3-12 | Relogin após expiração | Após EX3-10, informar credenciais válidas | Nova sessão criada; o menu volta a funcionar com o tempo reiniciado | OK |
| EX3-13 | Logout ao sair | Logar e sair com `S`; conferir `sessao:ativa` no Redis Insight | A chave não existe mais | OK |
| EX3-14 | Sessão usa EXPIRE | Após login, `TTL sessao:ativa` no Redis Insight ou CLI | TTL coerente com `SESSAO_TTL`; valor JSON com `usuario` e `token` | OK |
| EX3-15 | Renovação desativada (padrão) | `SESSAO_RENOVAR=false`; usar os menus continuamente por mais que o TTL | A sessão expira mesmo com uso contínuo | OK |
| EX3-16 | Renovação ativada | `SESSAO_RENOVAR=true`; usar os menus a cada poucos segundos | O tempo volta ao valor inicial a cada verificação; não expira em uso contínuo | OK |
| EX3-17 | TTL padrão | Remover `SESSAO_TTL` do `.env`; fazer login | O menu mostra expiração próxima de 1800s | OK |
| EX3-18 | Logout automático desligado | `SESSAO_LOGOUT_AUTO=false`; login; esperar expirar; escolher um menu | Sem aviso na hora; ao abrir o menu aparece `EXPIRADA` e pede novo login | OK |
| EX3-19 | Opção inválida nos menus | No menu principal digitar `9`; em um submenu digitar `9` | "Opção inválida."; o menu é exibido de novo | OK |

### Sincronização Mongo → Redis (opção 5)

| ID | Caso de teste | Passos | Resultado esperado | Status |
|----|---------------|--------|--------------------|--------|
| EX3-20 | Envio ao Redis | Logado, opção 5 | Imprime `fav_<email>  \|  end_<email>` por usuário e o total enviado | OK |
| EX3-21 | Mongo não perde dados | Após a opção 5, conferir os usuários no Mongo | Nada foi removido ou alterado no Mongo (a opção copia) | OK |
| EX3-22 | Conteúdo dos favoritos | `GET fav_<email>` | Lista JSON de strings com os ids dos produtos (`[]` se vazio) | OK |
| EX3-23 | Conteúdo dos endereços | `GET end_<email>` | Lista JSON com `logradouro`, `num`, `bairro`, `cidade`, `estado`, `cep`; acentos preservados | OK |
| EX3-24 | Usuário sem favoritos/endereços | Usuário sem esses campos; opção 5 | Chaves criadas com `[]`, sem erro | Não executado |
| EX3-25 | Usuário sem e-mail | Usuário sem o campo `email`; opção 5 | Usuário ignorado, sem erro | Não executado |

### Sincronização Redis → Mongo (opção 6)

| ID | Caso de teste | Passos | Resultado esperado | Status |
|----|---------------|--------|--------------------|--------|
| EX3-26 | Edição manual e retorno | Após 5, alterar `end_<email>` no Redis Insight (ex.: mudar a cidade); opção 6; conferir no Mongo | Endereço do usuário atualizado no Mongo | OK |
| EX3-27 | Favoritos voltam como ObjectId | Editar `fav_<email>` com o id de um produto existente; opção 6; conferir no Mongo | Campo `favoritos` é lista de `ObjectId`, não de strings | OK |
| EX3-28 | Sem alterações | Opção 5 e depois 6 sem editar | Mongo permanece idêntico ao original | OK |
| EX3-29 | JSON inválido | Gravar texto inválido em `fav_<email>`; opção 6 | `Ignorando fav_<email>: conteúdo inválido.`; Mongo não é alterado para essa chave | OK |
| EX3-30 | Id de favorito inválido | Colocar `["abc"]` em `fav_<email>`; opção 6 | Chave ignorada com a mesma mensagem; Mongo não é alterado | OK |
| EX3-31 | E-mail inexistente no Mongo | Criar `fav_naoexiste@x.com` no Redis; opção 6 | `usuário não encontrado no Mongo.`; nenhum usuário é criado | OK |

### CRUD no Redis (opção 7)

| ID | Caso de teste | Passos | Resultado esperado | Status |
|----|---------------|--------|--------------------|--------|
| EX3-32 | Create favorito | Opção 7 → 1; usuário (nome, CPF ou e-mail); tipo 1; id de produto válido | "Item criado em fav_<email>."; id aparece na lista JSON da chave | OK |
| EX3-33 | Create favorito duplicado ou id inválido | Repetir o mesmo id; depois informar `abc` | `Esse favorito já existe.` / `Id inválido...`; nada é gravado | Não executado |
| EX3-34 | Create endereço | Opção 7 → 1; tipo 2; preencher os 6 campos | Novo endereço adicionado à lista em `end_<email>` | OK |
| EX3-35 | Create para usuário inexistente | Opção 7 → 1; usuário que não está no Mongo | `Usuário não encontrado no Mongo...`; nenhuma chave criada | Não executado |
| EX3-36 | Read por usuário | Opção 7 → 2; responder `N`; informar nome (ex.: `paola`), CPF ou e-mail | Mostra `fav_` e `end_` do usuário, com itens numerados | OK |
| EX3-37 | Read de todos | Opção 7 → 2; responder `S` a "Deseja ver todos os usuários (S/N)?" | Lista todas as chaves `fav_*` e `end_*` | OK |
| EX3-38 | Update de endereço | Opção 7 → 3; tipo 2; escolher o número; mudar só a cidade (Enter nos demais) | Só a cidade muda; os outros campos permanecem | OK |
| EX3-39 | Update de favorito | Opção 7 → 3; tipo 1; número do item; novo id válido | O id do favorito é substituído | Não executado |
| EX3-40 | Delete de item | Opção 7 → 4; escolher o número do item | Item removido da lista; os demais permanecem | OK |
| EX3-41 | Delete da chave inteira | Opção 7 → 4; responder `T`; confirmar com `S` (testar `x` e `n` antes) | `x` é rejeitado; `n` cancela; `S` apaga a chave | Não executado |
| EX3-42 | Número ou tipo inválido | Informar número fora da lista ou tipo `9` | `Número inválido.` / `Opção inválida.`; nada muda | Não executado |
| EX3-43 | Chave com JSON quebrado | Gravar texto solto em `fav_<email>`; opção 7 → 2 | Mostra `(conteúdo inválido no Redis)` sem travar | OK |
| EX3-49 | Busca com mais de um resultado | Opção 7 → 2; `N`; digitar `pa` (nome comum a 2 usuários) | Lista numerada dos usuários; escolher o número | OK |
| EX3-50 | Update preserva todos os campos | Opção 7 → 3; tipo 2; mudar só a cidade; conferir `end_<email>` | Nenhum campo (nem o logradouro) é perdido | OK |
| EX3-44 | Ciclo completo | Opção 5 → opção 7 (criar, atualizar e apagar itens) → opção 6 → conferir no Mongo | O Mongo reflete exatamente as alterações feitas pelo CRUD | OK |

### Infraestrutura

| ID | Caso de teste | Passos | Resultado esperado | Status |
|----|---------------|--------|--------------------|--------|
| EX3-45 | Credenciais fora do código | `git grep -n "mongodb+srv"` | Nenhuma credencial real no código; tudo via `.env` | OK |
| EX3-46 | `.env` ignorado | `git status` com `.env` presente | `.env` não aparece como arquivo a versionar | Não executado |
| EX3-47 | `.env` da raiz vale sobre variáveis antigas | Alterar `SESSAO_TTL` no `.env` e rodar de novo | O título do login mostra o tempo novo | OK |
| EX3-48 | Redis indisponível | Parar o Redis ou errar o host; abrir o app | Mensagem clara de erro, sem traceback (requer tratamento de `ConnectionError`; hoje não implementado) | Não implementado |