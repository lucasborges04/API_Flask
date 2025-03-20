#Exercício 2: Cadastro de Usuários
from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Caminho do arquivo JSON que simula o banco de dados
USERS_FILE = 'usuarios.json'

# Função para carregar os dados do arquivo JSON
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as file:
            return json.load(file)
    return []

# Função para salvar os dados no arquivo JSON
def save_users(users):
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4)

# Rota para incluir um novo usuário
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    users = load_users()

    # Verifica se o nome de usuário já existe
    if any(user['username'] == data['username'] for user in users):
        return jsonify({"error": "Username already exists"}), 400

    users.append(data)
    save_users(users)
    return jsonify(data), 201

# Rota para consultar todos os usuários
@app.route('/users', methods=['GET'])
def get_users():
    users = load_users()
    return jsonify(users), 200

# Rota para consultar um usuário pelo ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    users = load_users()
    user = next((user for user in users if user['id'] == user_id), None)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200

# Rota para atualizar um usuário pelo ID
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    users = load_users()
    user = next((user for user in users if user['id'] == user_id), None)
    if user is None:
        return jsonify({"error": "User not found"}), 404

    user.update(data)
    save_users(users)
    return jsonify(user), 200

# Rota para excluir um usuário pelo ID
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    users = load_users()
    user = next((user for user in users if user['id'] == user_id), None)
    if user is None:
        return jsonify({"error": "User not found"}), 404

    users.remove(user)
    save_users(users)
    return jsonify({"message": "User deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)