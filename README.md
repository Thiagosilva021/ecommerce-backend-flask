# API de E-commerce

Uma API REST desenvolvida em Python utilizando Flask para simular um sistema de e-commerce.

O projeto permite autenticação de usuários, gerenciamento de produtos e operações de carrinho de compras.

## Tecnologias

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-CORS
- SQLite

---

## Funcionalidades

### Autenticação

- Login de usuário
- Logout
- Rotas protegidas

### Produtos

- Cadastrar produto
- Listar produtos
- Buscar produto por ID
- Atualizar produto
- Excluir produto

### Carrinho

- Adicionar produto
- Remover produto
- Visualizar carrinho
- Finalizar compra

---

## Estrutura do Projeto

```
.
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Como executar

### 1. Clone o projeto

```bash
git clone https://github.com/SEU-USUARIO/ecommerce-api.git
```

### 2. Entre na pasta

```bash
cd ecommerce-api
```

### 3. Crie um ambiente virtual

Windows

```bash
python -m venv venv
```

Linux/macOS

```bash
python3 -m venv venv
```

### 4. Ative o ambiente

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

### 5. Instale as dependências

```bash
pip install -r requirements.txt
```

### 6. Execute

```bash
python app.py
```

---

## Endpoints

### Login

```
POST /login
```

### Logout

```
POST /logout
```

### Produtos

```
GET    /api/products
GET    /api/products/<id>
POST   /api/products/add
PUT    /api/products/update/<id>
DELETE /api/products/delete/<id>
```

### Carrinho

```
POST   /api/cart/add/<id>
DELETE /api/cart/remove/<id>
GET    /api/cart
POST   /api/cart/checkout
```

---

## Objetivo

Este projeto foi desenvolvido com o objetivo de praticar conceitos de desenvolvimento backend utilizando Flask, incluindo autenticação, criação de APIs REST, integração com banco de dados e operações CRUD.

---

## Melhorias futuras

- Hash de senhas
- JWT Authentication
- PostgreSQL
- Docker
- Testes automatizados
- Frontend
- Deploy da aplicação
- Documentação Swagger

---

##  Autor

Thiago Silva

Estudante de Ciência da Computação.