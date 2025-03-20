from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Caminho do arquivo JSON que irá armazenar as tarefas
TASKS_FILE = 'tarefas.json'


# Função para ler as tarefas do arquivo
def read_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as file:
            return json.load(file)
    return []


# Função para escrever as tarefas no arquivo
def write_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)


# Rota para adicionar uma nova tarefa
@app.route('/tarefas', methods=['POST'])
def add_task():
    data = request.get_json()

    if 'titulo' not in data or 'descricao' not in data:
        return jsonify({"error": "Título e descrição são obrigatórios."}), 400

    tasks = read_tasks()
    task = {
        "id": len(tasks) + 1,  # ID gerado automaticamente
        "titulo": data['titulo'],
        "descricao": data['descricao'],
        "concluida": False  # A tarefa começa como não concluída
    }

    tasks.append(task)
    write_tasks(tasks)

    return jsonify({"message": "Tarefa adicionada com sucesso!"}), 201


# Rota para listar todas as tarefas
@app.route('/tarefas', methods=['GET'])
def list_tasks():
    tasks = read_tasks()
    return jsonify(tasks), 200


# Rota para marcar uma tarefa como concluída
@app.route('/tarefas/<int:task_id>/concluir', methods=['PUT'])
def mark_task_completed(task_id):
    tasks = read_tasks()

    for task in tasks:
        if task['id'] == task_id:
            task['concluida'] = True
            write_tasks(tasks)
            return jsonify({"message": "Tarefa marcada como concluída!"}), 200
   
    return jsonify({"error": "Tarefa não encontrada."}), 404


# Rota para excluir uma tarefa
@app.route('/tarefas/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = read_tasks()

    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            write_tasks(tasks)
            return jsonify({"message": "Tarefa excluída com sucesso!"}), 200

    return jsonify({"error": "Tarefa não encontrada."}), 404


if __name__ == '__main__':
    app.run(debug=True)