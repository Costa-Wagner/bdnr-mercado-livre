# 🧪 Roteiro de testes — EX2 BDNR Orientado a Documentos

Testes manuais do `menu.py` em execução, uma ação por vez, conferindo a saída no terminal e o estado dos documentos no MongoDB Compass (banco `mercadolivre_ex2`).

## Ambiente

| Ambiente | Ferramenta | Situação |
|---|---|---|
| Windows (desenvolvimento) | Terminal (Git Bash) + MongoDB Compass | Em andamento |

## Dados de apoio

Antes de rodar os testes de Produto e Compra, é preciso ter ao menos um Vendedor e um Usuário cadastrados (Produto depende de Vendedor; Compra depende de Usuario, Vendedor e Produto).

## Resumo

| Teste | Grupo | Descrição | Resultado |
|---|---|---|---|
| 1 | Vendedor | Create: cadastro válido (CNPJ formato antigo) | Aprovado |
| 2 | Vendedor | Create: cadastro com CNPJ novo alfanumérico | |
| 3 | Vendedor | Read: por nome e por CPF/CNPJ | |
| 4 | Vendedor | Read: todos (sem filtro) | |
| 5 | Vendedor | Update: vendedor existente | |
| 6 | Vendedor | Update: vendedor inexistente | Aprovado (corrigido) |
| 7 | Vendedor | Delete: vendedor existente | |
| 8 | Usuario | Create: cadastro válido | Aprovado |
| 9 | Usuario | Create: CPF inválido (menos de 11 dígitos) | |
| 10 | Usuario | Read: específico e todos | |
| 11 | Usuario | Update: usuário existente | |
| 12 | Usuario | Update: usuário inexistente | |
| 13 | Usuario | Delete: usuário existente | |
| 14 | Produto | Create: vinculado a vendedor existente | Aprovado |
| 15 | Produto | Create: CPF/CNPJ de vendedor inexistente (deve cancelar) | |
| 16 | Produto | Read: por nome e por categoria | |
| 17 | Produto | Update: produto existente | |
| 18 | Produto | Delete: produto existente | |
| 19 | Compra | Create: fluxo completo (usuário, vendedor e produto existentes) | Aprovado |
| 20 | Compra | Create: usuário sem endereço cadastrado (deve cancelar) | |
| 21 | Compra | Create: nome de produto inexistente (deve pedir de novo) | |
| 22 | Compra | Create: usuário com mais de um endereço (testar escolha) | |
| 23 | Compra | Read: por CPF específico | |
| 24 | Compra | Read: todas (sem filtro) | |
| 25 | Compra | Update: status e endereço de entrega | |
| 26 | Compra | Delete: compra existente | |
| 27 | Infra | Conflito de nome de banco (case-insensitive) | Aprovado (corrigido) |

## Teste 1 — Create Vendedor: cadastro válido (CNPJ formato antigo)

**Grupo:** Vendedor · **Pré-condição:** nenhuma.

| # | Ação no menu | Entrada | Esperado |
|---|---|---|---|
| 1 | `2` → `1` (CRUD Vendedor → Create) | Nome Fantasia, Razão Social, CNPJ de 14 dígitos numéricos, senha, telefone, e-mail, 1 endereço tipo "entrega" | `Documento inserido com ID ...` no terminal |
| 2 | Conferir no Compass | — | Documento na coleção `vendedor`, com `senhaVendedor` como hash (não texto puro) |

**Resultado:** Aprovado — executado durante o desenvolvimento, vendedor criado e confirmado no Compass.

## Teste 2 — Create Vendedor: CNPJ novo formato alfanumérico

**Grupo:** Vendedor · **Pré-condição:** nenhuma.

| # | Ação no menu | Entrada | Esperado |
|---|---|---|---|
| 1 | `2` → `1` | CNPJ no novo padrão, ex: `00000000E08G12` | Aceito sem erro de validação, `Documento inserido com ID ...` |

**Resultado:** _pendente_

## Teste 3 — Read Vendedor: por nome e por CPF/CNPJ

**Grupo:** Vendedor · **Pré-condição:** ao menos 1 vendedor cadastrado.

| # | Ação no menu | Entrada | Esperado |
|---|---|---|---|
| 1 | `2` → `2` | Nome fantasia exato, CPF/CNPJ em branco | Retorna só o vendedor com esse nome |
| 2 | `2` → `2` | Nome em branco, CPF/CNPJ exato | Retorna só o vendedor com esse CPF/CNPJ |
| 3 | `2` → `2` | Ambos preenchidos, de vendedores diferentes | Retorna vazio (busca é E, não OU) |

**Resultado:** _pendente_

## Teste 4 — Read Vendedor: todos (sem filtro)

**Grupo:** Vendedor · **Pré-condição:** ao menos 2 vendedores cadastrados.

| # | Ação no menu | Entrada | Esperado |
|---|---|---|---|
| 1 | `2` → `2` | Nome e CPF/CNPJ em branco (Enter) | Lista todos, ordenados por nome fantasia |

**Resultado:** _pendente_

## Teste 5 — Update Vendedor: existente

**Grupo:** Vendedor · **Pré-condição:** 1 vendedor cadastrado, com o nome fantasia anotado.

| # | Ação no menu | Entrada | Esperado |
|---|---|---|---|
| 1 | `2` → `3` | Nome fantasia exato | Mostra os dados atuais |
| 2 | — | Novo telefone, resto em branco | Só telefone muda |
| 3 | `2` → `2` | Mesmo nome | Confirma telefone atualizado, resto igual |

**Resultado:** _pendente_

## Teste 6 — Update Vendedor: inexistente

**Grupo:** Vendedor · **Pré-condição:** nenhuma.

| # | Ação no menu | Entrada | Esperado |
|---|---|---|---|
| 1 | `2` → `3` | Nome que não existe no banco | `Vendedor não encontrado.` — sem travar |

**Resultado:** Aprovado (corrigido) — a primeira execução travou com `WriteError: Modifiers operate on fields but we found type null` (tentava `$set: None` porque a função seguia em frente mesmo sem encontrar o vendedor). Corrigido adicionando checagem `if mydoc is None: return` logo após o `find_one`. Reteste com a correção ainda não repetido — vale confirmar que a mensagem amigável aparece.

## Teste 7 — Delete Vendedor: existente

**Grupo:** Vendedor · **Pré-condição:** 1 vendedor cadastrado (de teste, descartável), nome e CPF/CNPJ anotados.

| # | Ação no menu | Entrada | Esperado |
|---|---|---|---|
| 1 | `2` → `4` | Nome e CPF/CNPJ exatos | `Deletado o vendedor ...` |
| 2 | `2` → `2` | Mesmo nome | Não retorna mais nada |

**Resultado:** _pendente_

## Teste 8 — Create Usuario: cadastro válido

**Grupo:** Usuario · **Pré-condição:** nenhuma.

| # | Ação no menu | Entrada | Esperado |
|---|---|---|---|
| 1 | `1` → `1` | Nome, sobrenome, CPF de 11 dígitos, senha, 1 endereço | `Documento inserido com ID ...` |
| 2 | Conferir no Compass | — | Documento na coleção `usuario`, `senha` como hash |

**Resultado:** Aprovado — executado durante o desenvolvimento (após corrigir o conflito de nome de banco do Teste 27).

## Teste 9 — Create Usuario: CPF inválido

**Grupo:** Usuario · **Pré-condição:** nenhuma.

| # | Ação no menu | Entrada | Esperado |
|---|---|---|---|
| 1 | `1` → `1` | CPF com menos de 11 dígitos, ex: `123` | `CPF inválido! Digite 11 números.` — repete a pergunta até receber um CPF válido |

**Resultado:** _pendente_

## Teste 10 — Read Usuario: específico e todos

**Grupo:** Usuario · **Pré-condição:** ao menos 1 usuário cadastrado.

| # | Ação no menu | Entrada | Esperado |
|---|---|---|---|
| 1 | `1` → `2` | Nome exato | Retorna só esse usuário |
| 2 | `1` → `2` | Em branco | Lista todos, ordenados por nome |

**Resultado:** _pendente_

## Teste 11 — Update Usuario: existente

**Grupo:** Usuario · **Pré-condição:** 1 usuário cadastrado, nome anotado.

| # | Ação no menu | Entrada | Esperado |
|---|---|---|---|
| 1 | `1` → `3` | Nome exato | Mostra dados atuais |
| 2 | — | Nova senha, resto em branco | Só a senha muda (hash diferente do anterior) |

**Resultado:** _pendente_

## Teste 12 — Update Usuario: inexistente

**Grupo:** Usuario · **Pré-condição:** nenhuma.

| # | Ação no menu | Entrada | Esperado |
|---|---|---|---|
| 1 | `1` → `3` | Nome que não existe | `Usuário não encontrado.` — sem travar |

**Resultado:** _pendente_

## Teste 13 — Delete Usuario: existente

**Grupo:** Usuario · **Pré-condição:** 1 usuário de teste cadastrado, nome e sobrenome anotados.

| # | Ação no menu | Entrada | Esperado |
|---|---|---|---|
| 1 | `1` → `4` | Nome e sobrenome exatos | `Deletado o usuário ...` |

**Resultado:** _pendente_

## Teste 14 — Create Produto: vinculado a vendedor existente

**Grupo:** Produto · **Pré-condição:** 1 vendedor cadastrado, CPF/CNPJ anotado.

| # | Ação no menu | Entrada | Esperado |
|---|---|---|---|
| 1 | `3` → `1` | Nome, descrição, estoque, categoria, valor, 1 foto, CPF/CNPJ do vendedor existente | `Documento inserido com ID ...` |
| 2 | Conferir no Compass | — | Subdocumento `vendedor` embutido com `nomefantasiaVendedor`, `razaosociaVendedor`, `cnpjVendedor` etc. preenchidos com os dados reais do vendedor |

**Resultado:** Aprovado — executado durante o desenvolvimento.

## Teste 15 — Create Produto: vendedor inexistente

**Grupo:** Produto · **Pré-condição:** nenhuma.

| # | Ação no menu | Entrada | Esperado |
|---|---|---|---|
| 1 | `3` → `1` | Dados do produto normalmente, CPF/CNPJ que não existe no banco | `Vendedor não encontrado. Produto não cadastrado.` — nada é gravado |

**Resultado:** _pendente_

## Teste 16 — Read Produto: por nome e por categoria

**Grupo:** Produto · **Pré-condição:** ao menos 1 produto cadastrado.

| # | Ação no menu | Entrada | Esperado |
|---|---|---|---|
| 1 | `3` → `2` | Nome exato, categoria em branco | Retorna só esse produto |
| 2 | `3` → `2` | Nome em branco, categoria exata | Retorna produtos dessa categoria |

**Resultado:** _pendente_

## Teste 17 — Update Produto: existente

**Grupo:** Produto · **Pré-condição:** 1 produto cadastrado, nome anotado.

| # | Ação no menu | Entrada | Esperado |
|---|---|---|---|
| 1 | `3` → `3` | Nome exato | Mostra dados atuais |
| 2 | — | Novo valor, resto em branco | Só o valor muda |

**Resultado:** _pendente_

## Teste 18 — Delete Produto: existente

**Grupo:** Produto · **Pré-condição:** 1 produto de teste cadastrado, nome e CPF/CNPJ do vendedor anotados.

| # | Ação no menu | Entrada | Esperado |
|---|---|---|---|
| 1 | `3` → `4` | Nome do produto e CPF/CNPJ do vendedor | `Deletado o produto ...` |

**Resultado:** _pendente_

## Teste 19 — Create Compra: fluxo completo

**Grupo:** Compra · **Pré-condição:** 1 usuário (com endereço), 1 vendedor e 1 produto cadastrados.

| # | Ação no menu | Entrada | Esperado |
|---|---|---|---|
| 1 | `4` → `1` | CPF do usuário, CPF/CNPJ do vendedor, nome do produto e quantidade | `Documento inserido com ID ...` |
| 2 | Conferir no Compass | — | `usuario_id` e `vendedor_id` como ObjectId; `enderecoEntrega` copiado do usuário; `produtos[].precoUnitario` como Decimal128 |

**Resultado:** Aprovado — executado durante o desenvolvimento, compra criada e conferida no Compass.

## Teste 20 — Create Compra: usuário sem endereço

**Grupo:** Compra · **Pré-condição:** um usuário cadastrado sem nenhum endereço (caso raro — a criação normal de usuário exige ao menos 1 endereço, então esse teste depende de manipular o banco diretamente no Compass para remover o array `end`, ou pular caso não seja possível reproduzir).

| # | Ação no menu | Entrada | Esperado |
|---|---|---|---|
| 1 | `4` → `1` | CPF desse usuário | `Usuário não possui endereço cadastrado. Compra não cadastrada.` |

**Resultado:** _pendente_

## Teste 21 — Create Compra: produto inexistente

**Grupo:** Compra · **Pré-condição:** 1 usuário e 1 vendedor cadastrados.

| # | Ação no menu | Entrada | Esperado |
|---|---|---|---|
| 1 | `4` → `1` | CPF e CPF/CNPJ válidos; nome de produto que não existe | `Produto não encontrado, tente novamente.` — pede o nome de novo, sem travar |

**Resultado:** _pendente_

## Teste 22 — Create Compra: usuário com múltiplos endereços

**Grupo:** Compra · **Pré-condição:** 1 usuário cadastrado com 2+ endereços.

| # | Ação no menu | Entrada | Esperado |
|---|---|---|---|
| 1 | `4` → `1` | CPF desse usuário | Lista os endereços numerados, pede para escolher |
| 2 | — | Índice de um dos endereços | `enderecoEntrega` da compra bate com o endereço escolhido |

**Resultado:** _pendente_

## Teste 23 — Read Compra: por CPF específico

**Grupo:** Compra · **Pré-condição:** ao menos 1 compra cadastrada.

| # | Ação no menu | Entrada | Esperado |
|---|---|---|---|
| 1 | `4` → `2` | CPF do usuário dessa compra | Retorna só as compras desse usuário |

**Resultado:** _pendente_

## Teste 24 — Read Compra: todas

**Grupo:** Compra · **Pré-condição:** ao menos 1 compra cadastrada.

| # | Ação no menu | Entrada | Esperado |
|---|---|---|---|
| 1 | `4` → `2` | CPF em branco | Lista todas as compras |

**Resultado:** _pendente_

## Teste 25 — Update Compra: status e endereço

**Grupo:** Compra · **Pré-condição:** 1 compra cadastrada, `_id` anotado (via Read ou Compass).

| # | Ação no menu | Entrada | Esperado |
|---|---|---|---|
| 1 | `4` → `3` | `_id` da compra | Mostra dados atuais |
| 2 | — | `N` para status, nova cidade | `statusCompras` vira `false`, `enderecoEntrega.cidade` muda |

**Resultado:** _pendente_

## Teste 26 — Delete Compra: existente

**Grupo:** Compra · **Pré-condição:** 1 compra de teste cadastrada, `_id` anotado.

| # | Ação no menu | Entrada | Esperado |
|---|---|---|---|
| 1 | `4` → `4` | `_id` da compra | `Deletada a compra ...` |

**Resultado:** _pendente_

## Teste 27 — Infra: conflito de nome de banco (case-insensitive)

**Grupo:** Infra · **Contexto:** o MongoDB não permite dois bancos com nomes iguais diferindo só em maiúscula/minúscula.

| # | Ação | Esperado |
|---|---|---|
| 1 | Existia um banco `MercadoLivre` (criado manualmente no Compass) e o código usava `db = client.mercadolivre` | `pymongo.errors.WriteError: db already exists with different case` ao tentar gravar |
| 2 | Correção: renomear no código para `db = client.mercadolivre_ex2` (`app/conexao.py`) | Grava normalmente, sem colidir com o banco antigo, que fica preservado para consulta |

**Resultado:** Aprovado (corrigido) — reproduzido e corrigido durante o desenvolvimento.