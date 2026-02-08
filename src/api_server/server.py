from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields, reqparse
import json
import os
from datetime import datetime
from typing import Dict, List, Any

app = Flask(__name__)
api = Api(app, version='1.0', title='Test API',
          description='A simple test API for local testing')

# Namespace для API
ns = api.namespace('api', description='API operations')


# Функция для сериализации datetime объектов
def serialize_datetime(obj):
    """Сериализовать datetime объекты в ISO строки"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def serialize_data(data: Any) -> Any:
    """Рекурсивно сериализовать данные с datetime объектами"""
    if isinstance(data, dict):
        return {key: serialize_data(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [serialize_data(item) for item in data]
    elif isinstance(data, datetime):
        return data.isoformat()
    else:
        return data


# Модели данных
user_model = api.model('User', {
    'id': fields.Integer(readonly=True, description='User ID'),
    'username': fields.String(required=True, description='Username'),
    'email': fields.String(required=True, description='Email'),
    'created_at': fields.DateTime(readonly=True, description='Creation date'),
    'updated_at': fields.DateTime(readonly=True, description='Last update date')
})

user_update_model = api.model('UserUpdate', {
    'username': fields.String(description='Username'),
    'email': fields.String(description='Email')
})

product_model = api.model('Product', {
    'id': fields.Integer(readonly=True, description='Product ID'),
    'name': fields.String(required=True, description='Product name'),
    'price': fields.Float(required=True, description='Product price'),
    'in_stock': fields.Boolean(description='Availability'),
    'updated_at': fields.DateTime(readonly=True, description='Last update date')
})

product_update_model = api.model('ProductUpdate', {
    'name': fields.String(description='Product name'),
    'price': fields.Float(description='Product price'),
    'in_stock': fields.Boolean(description='Availability')
})

# Тестовые данные
users = [
    {
        'id': 1,
        'username': 'john_doe',
        'email': 'john@example.com',
        'created_at': datetime.now(),
        'updated_at': datetime.now()
    },
    {
        'id': 2,
        'username': 'jane_smith',
        'email': 'jane@example.com',
        'created_at': datetime.now(),
        'updated_at': datetime.now()
    },
    {
        'id': 3,
        'username': 'bob_wilson',
        'email': 'bob@example.com',
        'created_at': datetime.now(),
        'updated_at': datetime.now()
    }
]

products = [
    {
        'id': 1,
        'name': 'Laptop',
        'price': 999.99,
        'in_stock': True,
        'updated_at': datetime.now()
    },
    {
        'id': 2,
        'name': 'Mouse',
        'price': 25.50,
        'in_stock': True,
        'updated_at': datetime.now()
    },
    {
        'id': 3,
        'name': 'Keyboard',
        'price': 75.00,
        'in_stock': False,
        'updated_at': datetime.now()
    },
    {
        'id': 4,
        'name': 'Monitor',
        'price': 299.99,
        'in_stock': True,
        'updated_at': datetime.now()
    }
]


# Вспомогательные функции
def find_user_by_id(user_id):
    """Найти пользователя по ID"""
    for user in users:
        if user['id'] == user_id:
            return user
    return None


def find_user_index(user_id):
    """Найти индекс пользователя по ID"""
    for i, user in enumerate(users):
        if user['id'] == user_id:
            return i
    return -1


def find_product_by_id(product_id):
    """Найти продукт по ID"""
    for product in products:
        if product['id'] == product_id:
            return product
    return None


def find_product_index(product_id):
    """Найти индекс продукта по ID"""
    for i, product in enumerate(products):
        if product['id'] == product_id:
            return i
    return -1


@ns.route('/users')
class UserList(Resource):
    @ns.doc('list_users')
    @ns.marshal_list_with(user_model)
    def get(self):
        """Получить список всех пользователей"""
        return serialize_data(users)

    @ns.doc('create_user')
    @ns.expect(user_model)
    @ns.marshal_with(user_model, code=201)
    def post(self):
        """Создать нового пользователя"""
        data = api.payload
        now = datetime.now()
        new_user = {
            'id': len(users) + 1,
            'username': data['username'],
            'email': data['email'],
            'created_at': now,
            'updated_at': now
        }
        users.append(new_user)
        return serialize_data(new_user), 201

# просто так 3 5 Feature: шаг 1 Rebase: шаг 2
# rebase v2.0: шаг 1
@ns.route('/users/<int:user_id>')
@ns.response(404, 'User not found')
@ns.param('user_id', 'The user identifier')
class User(Resource):
    @ns.doc('get_user')
    @ns.marshal_with(user_model)
    def get(self, user_id):
        """Получить пользователя по ID"""
        user = find_user_by_id(user_id)
        if not user:
            api.abort(404, f"User {user_id} not found")
        return serialize_data(user)

    @ns.doc('delete_user')
    @ns.response(204, 'User deleted')
    def delete(self, user_id):
        """Удалить пользователя"""
        user_index = find_user_index(user_id)
        if user_index == -1:
            api.abort(404, f"User {user_id} not found")
        users.pop(user_index)
        return '', 204

    @ns.doc('update_user_full')
    @ns.expect(user_model)
    @ns.marshal_with(user_model)
    def put(self, user_id):
        """Полное обновление пользователя (PUT)"""
        user_index = find_user_index(user_id)
        if user_index == -1:
            api.abort(404, f"User {user_id} not found")

        data = api.payload
        # PUT требует всех полей для полной замены
        if 'username' not in data or 'email' not in data:
            api.abort(400, 'PUT requires all fields: username and email')

        # Сохраняем оригинальную дату создания
        original_created_at = users[user_index]['created_at']

        # Полностью заменяем объект
        users[user_index] = {
            'id': user_id,
            'username': data['username'],
            'email': data['email'],
            'created_at': original_created_at,
            'updated_at': datetime.now()
        }

        return serialize_data(users[user_index])

    @ns.doc('update_user_partial')
    @ns.expect(user_update_model)
    @ns.marshal_with(user_model)
    def patch(self, user_id):
        """Частичное обновление пользователя (PATCH)"""
        user_index = find_user_index(user_id)
        if user_index == -1:
            api.abort(404, f"User {user_id} not found")

        data = api.payload
        if not data:
            api.abort(400, 'No fields provided for update')

        # Обновляем только предоставленные поля
        if 'username' in data:
            users[user_index]['username'] = data['username']

        if 'email' in data:
            users[user_index]['email'] = data['email']

        # Обновляем timestamp
        users[user_index]['updated_at'] = datetime.now()

        return serialize_data(users[user_index])


@ns.route('/products')
class ProductList(Resource):
    @ns.doc('list_products')
    @ns.marshal_list_with(product_model)
    def get(self):
        """Получить список всех продуктов"""
        return serialize_data(products)

    @ns.doc('create_product')
    @ns.expect(product_model)
    @ns.marshal_with(product_model, code=201)
    def post(self):
        """Создать новый продукт"""
        data = api.payload
        new_product = {
            'id': len(products) + 1,
            'name': data['name'],
            'price': data['price'],
            'in_stock': data.get('in_stock', True),
            'updated_at': datetime.now()
        }
        products.append(new_product)
        return serialize_data(new_product), 201


@ns.route('/products/<int:product_id>')
@ns.response(404, 'Product not found')
class Product(Resource):
    @ns.doc('get_product')
    @ns.marshal_with(product_model)
    def get(self, product_id):
        """Получить продукт по ID"""
        product = find_product_by_id(product_id)
        if not product:
            api.abort(404, f"Product {product_id} not found")
        return serialize_data(product)

    @ns.doc('delete_product')
    @ns.response(204, 'Product deleted')
    def delete(self, product_id):
        """Удалить продукт"""
        product_index = find_product_index(product_id)
        if product_index == -1:
            api.abort(404, f"Product {product_id} not found")
        products.pop(product_index)
        return '', 204

    @ns.doc('update_product_full')
    @ns.expect(product_model)
    @ns.marshal_with(product_model)
    def put(self, product_id):
        """Полное обновление продукта (PUT)"""
        product_index = find_product_index(product_id)
        if product_index == -1:
            api.abort(404, f"Product {product_id} not found")

        data = api.payload
        # PUT требует всех обязательных полей
        if 'name' not in data or 'price' not in data:
            api.abort(400, 'PUT requires all fields: name and price')

        # Полностью заменяем объект
        products[product_index] = {
            'id': product_id,
            'name': data['name'],
            'price': data['price'],
            'in_stock': data.get('in_stock', True),
            'updated_at': datetime.now()
        }

        return serialize_data(products[product_index])

    @ns.doc('update_product_partial')
    @ns.expect(product_update_model)
    @ns.marshal_with(product_model)
    def patch(self, product_id):
        """Частичное обновление продукта (PATCH)"""
        product_index = find_product_index(product_id)
        if product_index == -1:
            api.abort(404, f"Product {product_id} not found")

        data = api.payload
        if not data:
            api.abort(400, 'No fields provided for update')

        # Обновляем только предоставленные поля
        if 'name' in data:
            products[product_index]['name'] = data['name']

        if 'price' in data:
            products[product_index]['price'] = data['price']

        if 'in_stock' in data:
            products[product_index]['in_stock'] = data['in_stock']

        # Обновляем timestamp
        products[product_index]['updated_at'] = datetime.now()

        return serialize_data(products[product_index])


@ns.route('/health')
class HealthCheck(Resource):
    @ns.doc('health_check')
    def get(self):
        """Проверка здоровья API"""
        return serialize_data({
            'status': 'healthy',
            'timestamp': datetime.now(),
            'endpoints': {
                'users': '/api/users',
                'products': '/api/products',
                'health': '/api/health',
                'echo': '/api/echo',
                'search': '/api/search',
                'stats': '/api/stats'
            }
        })


@ns.route('/echo')
class Echo(Resource):
    @ns.doc('echo')
    @ns.expect(api.model('EchoData', {
        'message': fields.String(required=True, description='Message to echo'),
        'data': fields.Raw(description='Additional data')
    }))
    def post(self):
        """Эхо-запрос, возвращает отправленные данные"""
        data = api.payload
        return serialize_data({
            'echo': data.get('message', ''),
            'received_data': data,
            'timestamp': datetime.now(),
            'method': 'POST'
        })

    @ns.doc('echo_get')
    @ns.param('message', 'Message to echo')
    @ns.param('data', 'Additional data (JSON string)')
    def get(self):
        """Эхо-запрос через GET"""
        message = request.args.get('message', 'Hello!')
        data_str = request.args.get('data', '{}')

        try:
            additional_data = json.loads(data_str)
        except:
            additional_data = {'error': 'Invalid JSON'}

        return serialize_data({
            'echo': message,
            'received_data': additional_data,
            'timestamp': datetime.now(),
            'method': 'GET'
        })


@ns.route('/stats')
class Stats(Resource):
    @ns.doc('get_stats')
    def get(self):
        """Получить статистику API"""
        return serialize_data({
            'users_count': len(users),
            'products_count': len(products),
            'server_time': datetime.now(),
            'memory_info': {
                'users_memory': len(str(users)),
                'products_memory': len(str(products))
            }
        })


@ns.route('/search')
class Search(Resource):
    @ns.doc('search_users')
    @ns.param('q', 'Search query')
    @ns.param('type', 'Type to search: users or products')
    def get(self):
        """Поиск по пользователям и продуктам"""
        query = request.args.get('q', '').lower()
        search_type = request.args.get('type', 'both')

        results = {}

        if search_type in ['users', 'both']:
            user_results = []
            for user in users:
                if (query in user['username'].lower() or
                        query in user['email'].lower()):
                    # Создаем копию пользователя с сериализованными datetime
                    user_copy = user.copy()
                    user_results.append(user_copy)
            results['users'] = user_results

        if search_type in ['products', 'both']:
            product_results = []
            for product in products:
                if query in product['name'].lower():
                    # Создаем копию продукта с сериализованными datetime
                    product_copy = product.copy()
                    product_results.append(product_copy)
            results['products'] = product_results

        # Сериализуем все данные перед возвратом
        return serialize_data({
            'query': query,
            'type': search_type,
            'results': results,
            'total': len(results.get('users', [])) + len(results.get('products', []))
        })


# Альтернативная версия с JSONEncoder
class CustomJSONEncoder(json.JSONEncoder):
    """Кастомный JSON encoder для обработки datetime"""

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


# Устанавливаем кастомный JSON encoder для Flask
app.json_encoder = CustomJSONEncoder


# Обработчики ошибок
@app.errorhandler(404)
def not_found(error):
    return {'error': 'Not Found', 'message': str(error)}, 404


@app.errorhandler(400)
def bad_request(error):
    return {'error': 'Bad Request', 'message': str(error)}, 400


@app.errorhandler(500)
def internal_error(error):
    return {'error': 'Internal Server Error', 'message': str(error)}, 500


if __name__ == '__main__':
    print("Starting API Server...")
    print("Available endpoints:")
    print("  GET  /api/health     - Health check")
    print("  GET  /api/users      - List all users")
    print("  POST /api/users      - Create user")
    print("  GET  /api/users/{id} - Get user")
    print("  PUT  /api/users/{id} - Full update user")
    print("  PATCH /api/users/{id} - Partial update user")
    print("  DELETE /api/users/{id} - Delete user")
    print("  GET  /api/products   - List all products")
    print("  POST /api/products   - Create product")
    print("  GET  /api/products/{id} - Get product")
    print("  PUT  /api/products/{id} - Full update product")
    print("  PATCH /api/products/{id} - Partial update product")
    print("  DELETE /api/products/{id} - Delete product")
    print("  POST /api/echo      - Echo endpoint")
    print("  GET  /api/echo      - Echo endpoint (GET)")
    print("  GET  /api/stats     - API statistics")
    print("  GET  /api/search    - Search endpoint")
    print("\nSwagger UI: http://localhost:5000/")

    app.run(debug=True, host='0.0.0.0', port=5000)