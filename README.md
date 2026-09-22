# 📚 DSM – Desenvolvimento de Software Multiplataforma – FATEC/SJC

Atividade prática **EX2** – Prof. Diogo Branquinho Ramos – Banco de Dados Não Relacional.

# 🛒 EX2 — BDNR Orientado a Documentos

REPOSITÓRIO ACADÊMICO · 3º sem DSM · Aplicação CRUD em linha de comando (Python e MongoDB) inspirada no modelo de marketplace do Mercado Livre: cadastro de usuários, vendedores, produtos e compras em banco não relacional, com validação de dados e senha hasheada.

## 📋 Requisitos

- Python 3.13.7
- Conta no MongoDB Atlas, com um cluster criado
- Ambiente virtual (`.venv`) recomendado

## 🛠 Tecnologias

### ⚙️ Back-end (Linguagem e Bibliotecas)

<p align="left">
<a href="https://www.python.org" target="_blank" rel="noopener noreferrer">
<img src="https://img.shields.io/badge/Python_3.13-3776AB?style=flat&logo=python&logoColor=white" alt="Python 3.13" height="25px">
</a>
<a href="https://pymongo.readthedocs.io" target="_blank" rel="noopener noreferrer">
<img src="https://img.shields.io/badge/PyMongo-47A248?style=flat&logo=mongodb&logoColor=white" alt="PyMongo" height="25px">
</a>
<a href="https://pypi.org/project/python-dotenv/" target="_blank" rel="noopener noreferrer">
<img src="https://img.shields.io/badge/python--dotenv-ECD53F?style=flat" alt="python-dotenv" height="25px">
</a>
</p>

### 🗄 Banco de dados

<p align="left">
<a href="https://www.mongodb.com/atlas" target="_blank" rel="noopener noreferrer">
<img src="https://img.shields.io/badge/MongoDB_Atlas-47A248?style=flat&logo=mongodb&logoColor=white" alt="MongoDB Atlas" height="25px">
</a>
</p>

## 🚀 Como executar

```bash
python -m venv .venv
source .venv/Scripts/activate      # Git Bash (Windows)
# .venv\Scripts\activate           # PowerShell/CMD (Windows)
pip install pymongo python-dotenv
python menu.py
```

Execute na raiz do projeto, a pasta que contém o `menu.py`. É necessário um arquivo `.env` na raiz (não versionado — ver `.env.example`) com a connection string do seu cluster:

```
MONGO_URI=mongodb+srv://usuario:senha@seucluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

- O menu roda continuamente no terminal até a opção "S" (sair) ser escolhida.
- O banco MongoDB é `mercadolivre_ex2`, criado automaticamente no cluster na primeira inserção (não precisa ser criado manualmente).

## 🗂 Estrutura do projeto

```
bdnr-mercado-livre/
├── .env                (não versionado)
├── .env.example
├── menu.py              menu principal (navegação)
├── app/
│   ├── __init__.py
│   ├── conexao.py       conexão compartilhada com o MongoDB
│   ├── validadores.py   validação de entradas (CPF, CNPJ, CEP, telefone etc.)
│   ├── usuario.py       CRUD de Usuario
│   ├── vendedor.py      CRUD de Vendedor
│   ├── produto.py       CRUD de Produto
│   └── compra.py        CRUD de Compra
└── referencias/          scripts de estudo, não usados pelo menu.py
    ├── obj-json.py
    ├── objeto.py
    └── objetos.py
```

## 🌳 Estrutura de dependências dos módulos

```bash
menu.py ──┬──► app.usuario   ──► app.conexao (db) + app.validadores
          ├──► app.vendedor  ──► app.conexao (db) + app.validadores
          ├──► app.produto   ──► app.conexao (db) + app.validadores
          │                       └─► consulta app.conexao.db.vendedor (embute dados do vendedor no produto)
          └──► app.compra    ──► app.conexao (db) + app.validadores
                                  └─► consulta db.usuario, db.vendedor, db.produto (referencia e embute dados)
```

## 🖥 Estrutura do menu

```bash
Menu Principal
├── 1 - CRUD Usuário    → 1 Create · 2 Read · 3 Update · 4 Delete
├── 2 - CRUD Vendedor   → 1 Create · 2 Read · 3 Update · 4 Delete
├── 3 - CRUD Produto    → 1 Create · 2 Read · 3 Update · 4 Delete
├── 4 - CRUD Compra     → 1 Create · 2 Read · 3 Update · 4 Delete
└── S - Sair
```

## 🗃 Modelo de dados

```
Usuario 1 ── * Compra (via usuario_id)
Vendedor 1 ── * Produto (dados do vendedor embutidos no produto)
Vendedor 1 ── * Compra (via vendedor_id)
Produto  1 ── * item dentro de Compra.produtos (produto_id referenciado, preço copiado no momento da compra)
```

`Produto.vendedor` é um subdocumento **embutido** (não uma referência), copiado do Vendedor no momento da criação do produto — decisão de modelagem que evita Join na leitura, ao custo de duplicação (se o vendedor mudar telefone, produtos já cadastrados não atualizam automaticamente).

`Compra.enderecoEntrega` também é embutido, copiado do endereço do Usuario no momento da compra — garante que o endereço da compra não muda se o usuário atualizar seu cadastro depois.

## 🔌 Coleções

### Usuario

| Campo | Tipo | Observação |
|---|---|---|
| `_id` | ObjectId | gerado automaticamente |
| `nome`, `sobrenome` | string | |
| `cpf` | string | 11 dígitos |
| `senha` | string | hash SHA-256 |
| `end` | array de objetos | `logradouro`, `num`, `bairro`, `cidade`, `estado`, `cep` |

### Vendedor

| Campo | Tipo | Observação |
|---|---|---|
| `_id` | ObjectId | gerado automaticamente |
| `nomeFantasiaVendedor`, `razaoSocialVendedor` | string | |
| `cpf_cnpjVendedor` | string | CPF (11 dígitos) ou CNPJ (14 caracteres, formato antigo numérico ou novo alfanumérico) |
| `senhaVendedor` | string | hash SHA-256 |
| `enderecoVendedor` | array de objetos | `tipo`, `logradouro`, `bairro`, `cidade`, `estado`, `cep` |
| `telefoneVendedor`, `emailVendedor` | string | |

### Produto

| Campo | Tipo | Observação |
|---|---|---|
| `_id` | ObjectId | gerado automaticamente |
| `nomeProduto`, `descricaoProduto`, `categoriaProduto` | string | |
| `estoqueProduto` | int | |
| `valorProduto` | float | |
| `fotoProduto` | array de string | URLs |
| `vendedor` | objeto embutido | `vendedor_id`, `nomefantasiaVendedor`, `razaosociaVendedor`, `cnpjVendedor`, `enderecoEnvioVendedor`, `telefoneVendedor`, `emailVendedor` |

### Compra

| Campo | Tipo | Observação |
|---|---|---|
| `_id` | ObjectId | gerado automaticamente |
| `dataCompras` | datetime | preenchida na criação |
| `statusCompras` | bool | `true` = ativa, `false` = cancelada |
| `enderecoEntrega` | objeto embutido | `logradouro`, `cidade` |
| `usuario_id`, `vendedor_id` | ObjectId | referências |
| `produtos` | array de objetos | `produto_id` (referência), `quantidade`, `precoUnitario` (Decimal128) |

## ✅ Validações (`app/validadores.py`)

| Função | Regra |
|---|---|
| `ler_texto` | apenas letras e espaços |
| `ler_numero` | apenas dígitos, tamanho opcionalmente fixo |
| `ler_cpf` | 11 dígitos |
| `ler_cpf_cnpj` / `cpf_cnpj_valido` | CPF: 11 dígitos. CNPJ: 14 caracteres (12 alfanuméricos + 2 dígitos verificadores), aceitando o novo padrão alfanumérico da Receita Federal (vigente desde jul/2026) |
| `ler_cep` | 8 dígitos |
| `ler_telefone` | apenas dígitos |
| `ler_logradouro` | não vazio, contém ao menos uma letra |
| `ler_sim_nao` | apenas "S" ou "N" |

## ⚠️ Tratamento de erros

| Situação | Comportamento |
|---|---|
| Vendedor não encontrado ao cadastrar Produto | Mensagem e cancela o cadastro |
| Usuário ou Vendedor não encontrado ao cadastrar Compra | Mensagem e cancela o cadastro |
| Usuário sem endereço cadastrado ao cadastrar Compra | Mensagem e cancela o cadastro |
| Produto não encontrado ao adicionar item à Compra | Mensagem, permite tentar outro nome |
| Registro não encontrado em Update (Usuario, Vendedor, Produto, Compra) | Mensagem "não encontrado", operação cancelada sem gravar |
| Entrada inválida (CPF, CNPJ, CEP, telefone, texto) | Repete a pergunta até receber um valor válido |

## 🧪 Testes

Os testes foram executados manualmente contra o menu em execução, uma ação por vez, conferindo a saída no terminal e o estado dos documentos no MongoDB Compass. O roteiro completo está em [testes.md](/docs/testes.md). 

## 💾 Persistência de dados

Os dados ficam no **MongoDB Atlas**, no banco `mercadolivre_ex2` — persistentes entre execuções (diferente de um banco em memória). As coleções e o banco são criados automaticamente na primeira inserção de cada uma.

## 🎯 Conceitos aplicados

- Python 3 e Programação Estruturada
- MongoDB (modelagem não relacional): embutimento vs. referência, decisão de modelagem por caso de uso
- PyMongo: `insert_one`, `find`, `find_one`, `update_one` com `$set`, `delete_one`
- Hashing de senha com `hashlib.sha256`
- Validação de entrada e tratamento de exceções (`try/except`, laços de repetição até entrada válida)
- Variáveis de ambiente com `python-dotenv`, separando credenciais do código
- Modularização em pacote Python (`app/`), separando conexão, validação e cada entidade