from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Caminho dos arquivos de persistência
PRODUCTS_FILE = 'produtos.json'
CART_FILE = 'carrinho.json'


# Função para ler os produtos do arquivo
def read_products():
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, 'r') as file:
            return json.load(file)
    return []


# Função para escrever os produtos no arquivo
def write_products(products):
    with open(PRODUCTS_FILE, 'w') as file:
        json.dump(products, file, indent=4)


# Função para ler o carrinho de compras
def read_cart():
    if os.path.exists(CART_FILE):
        with open(CART_FILE, 'r') as file:
            return json.load(file)
    return []


# Função para escrever o carrinho de compras no arquivo
def write_cart(cart):
    with open(CART_FILE, 'w') as file:
        json.dump(cart, file, indent=4)


# Rota para adicionar um produto
@app.route('/produtos', methods=['POST'])
def add_product():
    data = request.get_json()

    if 'nome' not in data or 'preco' not in data or 'estoque' not in data:
        return jsonify({"error": "Nome, preço e estoque são obrigatórios."}), 400

    products = read_products()
    product = {
        "id": len(products) + 1,  # ID gerado automaticamente
        "nome": data['nome'],
        "preco": data['preco'],
        "estoque": data['estoque']
    }

    products.append(product)
    write_products(products)

    return jsonify({"message": "Produto adicionado com sucesso!"}), 201


# Rota para listar todos os produtos
@app.route('/produtos', methods=['GET'])
def list_products():
    products = read_products()
    return jsonify(products), 200


# Rota para atualizar o estoque de um produto
@app.route('/produtos/<int:product_id>/estoque', methods=['PUT'])
def update_stock(product_id):
    data = request.get_json()

    if 'estoque' not in data:
        return jsonify({"error": "O campo 'estoque' é obrigatório."}), 400

    products = read_products()

    for product in products:
        if product['id'] == product_id:
            product['estoque'] = data['estoque']
            write_products(products)
            return jsonify({"message": "Estoque atualizado com sucesso!"}), 200
   
    return jsonify({"error": "Produto não encontrado."}), 404


# Rota para excluir um produto
@app.route('/produtos/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    products = read_products()

    for product in products:
        if product['id'] == product_id:
            products.remove(product)
            write_products(products)
            return jsonify({"message": "Produto excluído com sucesso!"}), 200

    return jsonify({"error": "Produto não encontrado."}), 404


# Rota para adicionar um produto ao carrinho
@app.route('/carrinho', methods=['POST'])
def add_to_cart():
    data = request.get_json()

    if 'produto_id' not in data or 'quantidade' not in data:
        return jsonify({"error": "Produto ID e quantidade são obrigatórios."}), 400

    products = read_products()
    cart = read_cart()

    # Verifica se o produto existe
    product = next((p for p in products if p['id'] == data['produto_id']), None)

    if not product:
        return jsonify({"error": "Produto não encontrado."}), 404

    # Verifica se há estoque suficiente
    if product['estoque'] < data['quantidade']:
        return jsonify({"error": "Estoque insuficiente."}), 400

    # Verifica se o produto já está no carrinho
    existing_item = next((item for item in cart if item['produto_id'] == data['produto_id']), None)

    if existing_item:
        existing_item['quantidade'] += data['quantidade']
    else:
        cart.append({
            "produto_id": data['produto_id'],
            "quantidade": data['quantidade']
        })

    # Atualiza o estoque do produto
    product['estoque'] -= data['quantidade']
    write_products(products)
    write_cart(cart)

    return jsonify({"message": "Produto adicionado ao carrinho com sucesso!"}), 201


# Rota para listar os itens no carrinho
@app.route('/carrinho', methods=['GET'])
def list_cart():
    cart = read_cart()
    products = read_products()

    cart_items = []

    for item in cart:
        product = next((p for p in products if p['id'] == item['produto_id']), None)
        if product:
            cart_items.append({
                "id": product['id'],
                "nome": product['nome'],
                "preco": product['preco'],
                "quantidade": item['quantidade'],
                "total": product['preco'] * item['quantidade']
            })

    return jsonify(cart_items), 200


# Rota para remover um item do carrinho
@app.route('/carrinho/<int:product_id>', methods=['DELETE'])
def remove_from_cart(product_id):
    cart = read_cart()

    for item in cart:
        if item['produto_id'] == product_id:
            cart.remove(item)
            write_cart(cart)
            return jsonify({"message": "Produto removido do carrinho com sucesso!"}), 200

    return jsonify({"error": "Produto não encontrado no carrinho."}), 404


if __name__ == '__main__':
    app.run(debug=True)