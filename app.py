# Importação
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

# Criação de uma instância da aplicação Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui' # Configuração da chave secreta para a aplicação Flask, usada para proteger sessões e cookies
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exemplo.db' # Configuração do URI do banco de dados SQLite

login_manager = LoginManager() # Criação de uma instância do LoginManager para gerenciar a autenticação de usuários
db = SQLAlchemy(app) # Criação de uma instância do SQLAlchemy para gerenciar o banco de dados
login_manager.init_app(app) # Inicialização do LoginManager com a aplicação Flask
login_manager.login_view = 'login' # Definição da rota de login para redirecionar usuários não autenticados
CORS(app) # Habilitação do CORS (Cross-Origin Resource Sharing) para permitir que a aplicação seja acessada de diferentes origens

# ============================
# Modelos de dados
# ===========================

# Definição do modelo de dados para a tabela "user" no banco de dados
class User(db.Model, UserMixin): 
    id = db.Column(db.Integer, primary_key=True) # Coluna "id" do tipo inteiro, que será a chave primária da tabela
    username = db.Column(db.String(100), nullable=False, unique=True) # Coluna "username" do tipo string com tamanho máximo de 100 caracteres, que deve ser única e não pode ser nula
    password = db.Column(db.String(100), nullable=False) # Coluna "password" do tipo string com tamanho máximo de 100 caracteres, que não pode ser nula
    cart = db.relationship('CartItem', backref='user', lazy=True) # Relacionamento com a tabela "CartItem", permitindo acessar os itens do carrinho de um usuário

# Definição do modelo de dados para a tabela "produto" no banco de dados
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Coluna "id" do tipo inteiro, que será a chave primária da tabela
    name = db.Column(db.String(120), nullable=False) # Coluna "name" do tipo string com tamanho máximo de 120 caracteres, que não pode ser nula
    price = db.Column(db.Float, nullable=False) # Coluna "price" do tipo float, que não pode ser nula
    description = db.Column(db.Text, nullable=True) # Coluna "description" do tipo text, que pode ser nula

# Definição do modelo de dados para a tabela "CartItem" no banco de dados
class CartItem(db.Model): 
    id = db.Column(db.Integer, primary_key=True) # Coluna "id" do tipo inteiro, que será a chave primária da tabela
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # Coluna "user_id" do tipo inteiro, que é uma chave estrangeira referenciando a tabela "user" e não pode ser nula
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False) # Coluna "product_id" do tipo inteiro, que é uma chave estrangeira referenciando a tabela "product" e não pode ser nula

# ===========================
# Rotas do login, logout
# ===========================

# Autenticação do usuário usando o Flask-Login
@login_manager.user_loader
def load_user(user_id): # Função que carrega o usuário a partir do ID fornecido
    return User.query.get(int(user_id)) # Função que carrega o usuário a partir do ID fornecido, retornando o objeto User correspondente do banco de dados

# Rota para realizar o login do usuário
@app.route("/login", methods=["POST"])
def login():
    data = request.json # Obtém os dados enviados na requisição em formato JSON
    username = data.get("username") # Obtém o nome de usuário do JSON recebido
    password = data.get("password") # Obtém a senha do JSON recebido

    user = User.query.filter_by(username=username).first() # Consulta o banco de dados para encontrar um usuário com o nome de usuário fornecido
    if user and user.password == password: # Verifica se o usuário existe e se a senha fornecida corresponde à senha armazenada no banco de dados
        login_user(user) # Realiza o login do usuário usando a função login_user do Flask-Login
        return jsonify({"message": "Login feito com sucesso!"}) # Retorna uma mensagem de sucesso em formato JSON
    return jsonify({"message": "Credenciais inválidas!"}), 401 # Retorna uma mensagem de erro em formato JSON com o código de status HTTP 401 (Não autorizado)

@app.route("/logout", methods=["POST"])
@login_required # Decorador que exige que o usuário esteja autenticado para acessar essa rota
def logout():
    logout_user() # Realiza o logout do usuário usando a função logout_user do Flask-Login
    return jsonify({"message": "Logout feito com sucesso!"}) # Retorna uma mensagem de sucesso em formato JSON

# ============================
# Rotas da api de produtos
# ===========================

# Rota para adicionar um novo produto ao banco de dados
@app.route("/api/products/add", methods=["POST"])
@login_required # Decorador que exige que o usuário esteja autenticado para acessar essa rota
def add_product(): 
    data = request.json # Obtém os dados enviados na requisição em formato JSON
    # Verifica se os campos "name" e "price" estão presentes nos dados recebidos
    if 'name' in data and 'price' in data:
        product = Product(name=data["name"], price=data["price"], description=data.get("description", ""))
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": "Produto adicionado com sucesso!"})
    return jsonify({"message": "Dados inválidos!"}), 400

# Rota para deletar um produto existente
@app.route("/api/products/delete/<int:product_id>", methods=["DELETE"]) 
@login_required # Decorador que exige que o usuário esteja autenticado para acessar essa rota
def delete_product(product_id):
    product = Product.query.get(product_id) # Obtém o produto com o ID especificado
    # Verifica se o produto existe no banco de dados
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Produto deletado com sucesso!"})
    return jsonify({"message": "Produto não encontrado!"}), 404

# Rota para obter os detalhes de um produto específico
@app.route("/api/products/<int:product_id>", methods=["GET"]) 
@login_required # Decorador que exige que o usuário esteja autenticado para acessar essa rota
def get_product_details(product_id):
    product = Product.query.get(product_id) # Obtém o produto com o ID especificado
    # Verifica se o produto existe no banco de dados
    if product: 
        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
        })
    return jsonify({"message": "Produto não encontrado!"}), 404

# Rota para atualizar os detalhes de um produto existente
@app.route("/api/products/update/<int:product_id>", methods=["PUT"])
@login_required # Decorador que exige que o usuário esteja autenticado para acessar essa rota
def update_product(product_id):
    product = Product.query.get(product_id) # Obtém o produto com o ID especificado
    # Verifica se o produto não existe no banco de dados, retornando uma mensagem de erro
    if not product:
        return jsonify({"message": "Produto não encontrado!"}), 404
    
    data = request.json# Obtém os dados enviados na requisição em formato JSON 
    # Atualiza os campos do produto com os dados recebidos, se estiverem presentes
    if 'name' in data:
        product.name = data['name']
    if 'price' in data:
        product.price = data['price']
    if 'description' in data:
        product.description = data['description']

    db.session.commit()
    return jsonify({"message": "Produto atualizado com sucesso!"})

# Rota para obter todos os produtos cadastrados no banco de dados
@app.route("/api/products", methods=["GET"]) 
def get_products():
     products = Product.query.all() # Obtém todos os produtos do banco de dados
     product_list = [] # Cria uma lista vazia para armazenar os dados dos produtos
     # Itera sobre cada produto obtido do banco de dados
     for product in products:
        product_data = {
            "id": product.id,
            "name": product.name,
            "price": product.price
        }
        product_list.append(product_data) # Adiciona os dados do produto à lista de produtos
     return jsonify(product_list) # Retorna a lista de produtos em formato JSON

# ==============================
# Rotas do carrinho de compras
# ==============================

# Rota para adicionar um produto ao carrinho de compras
@app.route("/api/cart/add/<int:product_id>", methods=["POST"]) 
@login_required # Decorador que exige que o usuário esteja autenticado para acessar essa rota
def add_to_cart(product_id):
    user = User.query.get(current_user.id) # Obtém o usuário atualmente autenticado
    product = Product.query.get(product_id) # Obtém o produto com o ID especificado
    # Verifica se o usuário e o produto existem no banco de dados
    if user and product:
        cart_item = CartItem(user_id=user.id, product_id=product.id) # Cria um novo item de carrinho associando o usuário e o produto
        db.session.add(cart_item) # Adiciona o item de carrinho à sessão do banco de dados
        db.session.commit() # Salva as alterações no banco de dados
        return jsonify({"message": "Produto adicionado ao carrinho com sucesso!"})
    return jsonify({"message": "Falha ao adicionar produto ao carrinho!"}), 400

# Rota para remover um produto do carrinho de compras
@app.route("/api/cart/remove/<int:product_id>", methods=["DELETE"])
@login_required # Decorador que exige que o usuário esteja autenticado para acessar essa rota
def remove_from_cart(product_id):
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first() # Obtém o item de carrinho correspondente ao usuário e ao produto especificado
    if cart_item: # Verifica se o item de carrinho existe no banco de dados
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({"message": "Produto removido do carrinho com sucesso!"})
    return jsonify({"message": "Falha ao remover produto do carrinho!"}), 400

# Rota para obter os itens do carrinho de compras do usuário autenticado
@app.route("/api/cart", methods=["GET"]) 
@login_required # Decorador que exige que o usuário esteja autenticado para acessar essa rota
def view_cart():
    user = User.query.get(current_user.id) # Obtém o usuário atualmente autenticado
    cart_items = user.cart # Obtém os itens do carrinho associados ao usuário
    cart_content = [] # Cria uma lista vazia para armazenar os dados dos itens do carrinho
    for cart_item in cart_items: # Itera sobre cada item do carrinho
        product = Product.query.get(cart_item.product_id) # Obtém o produto associado ao item do carrinho
        cart_content.append({
            "id": cart_item.id,
            "user_id": cart_item.user_id,
            "product_id": cart_item.product_id,
            "product_name": product.name,
            "product_price": product.price
        })
    return jsonify(cart_content) # Retorna a lista de itens do carrinho em formato JSON

# Rota para finalizar a compra dos itens do carrinho de compras
@app.route("/api/cart/checkout", methods=["POST"])
@login_required # Decorador que exige que o usuário esteja autenticado para acessar essa rota
def checkout():
    user = User.query.get(current_user.id) # Obtém o usuário atualmente autenticado
    cart_items = user.cart # Obtém os itens do carrinho associados ao usuário
    for cart_item in cart_items: # Itera sobre cada item do carrinho
        db.session.delete(cart_item) # Remove o item do carrinho do banco de dados
    db.session.commit() # Salva as alterações no banco de dados
    return jsonify({"message": "Finalização da compra bem-sucedida. O carrinho foi esvaziado."}) # Retorna uma mensagem de sucesso em formato JSON

# Iniciar o servidor Flask
if __name__ == "__main__":
    app.run(debug=True) # O parâmetro debug=True permite que o servidor seja reiniciado automaticamente quando houver alterações no código e fornece informações detalhadas sobre erros.
