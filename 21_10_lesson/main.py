from flask import Flask, jsonify, request

app = Flask(__name__)

# Хранилище данных в памяти
items = []
next_id = 1

# Получить список всех элементов (метод GET)
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items), 200

# Добавить новый элемент в список (метод POST)
@app.route('/items', methods=['POST'])
def add_item():
    global next_id
    data = request.get_json()
    
    # Проверка на наличие поля "name" в запросе
    if 'name' not in data:
        return jsonify({"error": "Поле 'name' обязательно"}), 400

    item = {
        "id": next_id,
        "name": data['name']
    }
    items.append(item)
    next_id += 1

    return jsonify(item), 201

# Запуск сервера
if __name__ == '__main__':
    app.run(debug=True)
