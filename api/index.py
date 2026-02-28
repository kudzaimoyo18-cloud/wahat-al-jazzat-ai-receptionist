"""
Vercel Serverless Functions for Wahat Al Jazzat AI Receptionist
"""

from http.server import BaseHTTPRequestHandler
import json
import os
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import requests
from urllib.parse import urlparse, parse_qs

# Database configuration
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci'
        )
        return conn
    except Error as e:
        print(f"Database connection error: {e}")
        return None

def execute_query(query: str, params: tuple = None, fetch: bool = False):
    conn = get_db_connection()
    if not conn:
        return None

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        if fetch:
            result = cursor.fetchall()
            conn.close()
            return result
        else:
            conn.commit()
            last_id = cursor.lastrowid
            conn.close()
            return last_id
    except Error as e:
        conn.close()
        print(f"Query execution error: {e}")
        return None

def handler(request):
    """Main handler for Vercel serverless function"""
    try:
        # Parse request
        method = request.method
        path = request.path
        headers = dict(request.headers)
        body = request.body.read().decode('utf-8') if request.body else ''

        # Handle CORS
        if method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, PUT, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type, Authorization'
                },
                'body': ''
            }

        # Route handling
        if path == '/health':
            return health_check()
        elif path == '/menu' and method == 'GET':
            return get_menu()
        elif path == '/chat' and method == 'POST':
            data = json.loads(body) if body else {}
            return chat(data)
        elif path.startswith('/orders'):
            if method == 'GET':
                return get_orders(request.query)
            elif method == 'PUT' and path.endswith('/status'):
                order_id = int(path.split('/')[2])
                data = json.loads(body) if body else {}
                return update_order_status(order_id, data)
        elif path.startswith('/orders/') and method == 'GET':
            order_id = int(path.split('/')[2])
            return get_order(order_id)
        elif path.startswith('/sessions'):
            if method == 'POST':
                data = json.loads(body) if body else {}
                return create_session(data)
            elif method == 'GET' and path.endswith('/orders'):
                session_id = path.split('/')[2]
                return get_session_orders(session_id)
            elif method == 'GET' and path.endswith('/conversation'):
                session_id = path.split('/')[2]
                return get_conversation(session_id)

        # 404 for unknown routes
        return {
            'statusCode': 404,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Not found'})
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }

# API Endpoints

def health_check():
    """Health check endpoint"""
    try:
        conn = get_db_connection()
        if conn:
            conn.close()
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'status': 'healthy', 'database': 'connected'})
            }
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'status': 'unhealthy', 'database': 'disconnected'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'status': 'unhealthy', 'error': str(e)})
        }

def get_menu():
    """Get all menu items"""
    query = """
        SELECT * FROM menu_items
        WHERE is_active = TRUE
        ORDER BY category, item_name
    """
    items = execute_query(query, fetch=True)

    if not items:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Failed to load menu'})
        }

    # Group by category
    categories = {}
    for item in items:
        category = item['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(item)

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'categories': categories})
    }

def chat(data):
    """Send message to AI receptionist via n8n"""
    try:
        n8n_base_url = os.getenv('N8N_BASE_URL')
        url = f"{n8n_base_url}/webhook/wahat-al-jazzat/chat"

        headers = {
            'Content-Type': 'application/json',
            'X-Session-ID': data.get('sessionId', '')
        }

        payload = {
            "message": data.get('message', ''),
            "customerInfo": data.get('customerInfo', {})
        }

        response = requests.post(url, json=payload, headers=headers, timeout=30)

        if response.status_code == 200:
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'body': json.dumps(response.json())
            }
        else:
            return {
                'statusCode': response.status_code,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': f"n8n error: {response.text}"})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': f"Failed to connect to n8n: {str(e)}"})
        }

def get_orders(query_params):
    """Get all orders or filter by status"""
    status = query_params.get('status', [None])[0] if query_params else None

    if status:
        query = """
            SELECT o.*, s.customer_name, s.phone_number
            FROM orders o
            JOIN sessions s ON o.session_id = s.session_id
            WHERE o.order_status = %s
            ORDER BY o.created_at DESC
        """
        orders = execute_query(query, (status,), fetch=True)
    else:
        query = """
            SELECT o.*, s.customer_name, s.phone_number
            FROM orders o
            JOIN sessions s ON o.session_id = s.session_id
            WHERE o.order_status IN ('pending', 'preparing', 'ready')
            ORDER BY o.created_at ASC
        """
        orders = execute_query(query, fetch=True)

    if not orders:
        orders = []

    # Get items for each order
    for order in orders:
        item_query = """
            SELECT oi.*, m.item_name
            FROM order_items oi
            JOIN menu_items m ON oi.item_id = m.id
            WHERE oi.order_id = %s
        """
        order['items'] = execute_query(item_query, (order['id'],), fetch=True) or []

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'orders': orders})
    }

def get_order(order_id):
    """Get specific order details"""
    query = """
        SELECT o.*, s.customer_name, s.phone_number
        FROM orders o
        JOIN sessions s ON o.session_id = s.session_id
        WHERE o.id = %s
    """
    orders = execute_query(query, (order_id,), fetch=True)

    if not orders:
        return {
            'statusCode': 404,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Order not found'})
        }

    order = orders[0]

    # Get order items
    item_query = """
        SELECT oi.*, m.item_name
        FROM order_items oi
        JOIN menu_items m ON oi.item_id = m.id
        WHERE oi.order_id = %s
    """
    order['items'] = execute_query(item_query, (order_id,), fetch=True) or []

    # Get status history
    status_query = """
        SELECT * FROM order_status_log
        WHERE order_id = %s
        ORDER BY created_at DESC
    """
    order['status_history'] = execute_query(status_query, (order_id,), fetch=True) or []

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(order)
    }

def update_order_status(order_id, data):
    """Update order status"""
    # Check if order exists
    check_query = "SELECT order_status FROM orders WHERE id = %s"
    existing = execute_query(check_query, (order_id,), fetch=True)

    if not existing:
        return {
            'statusCode': 404,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Order not found'})
        }

    old_status = existing[0]['order_status']
    new_status = data.get('status', '')
    notes = data.get('notes', '')

    # Update order status
    update_query = """
        UPDATE orders
        SET order_status = %s, updated_at = NOW()
        WHERE id = %s
    """
    execute_query(update_query, (new_status, order_id))

    # Log status change
    log_query = """
        INSERT INTO order_status_log
        (order_id, previous_status, new_status, changed_by, notes)
        VALUES (%s, %s, %s, 'kitchen', %s)
    """
    execute_query(log_query, (order_id, old_status, new_status, notes))

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({
            'success': True,
            'message': 'Order status updated successfully',
            'orderId': order_id,
            'oldStatus': old_status,
            'newStatus': new_status
        })
    }

def create_session(data):
    """Create a new customer session"""
    import uuid
    session_id = str(uuid.uuid4())

    query = """
        INSERT INTO sessions (session_id, customer_name, phone_number, email)
        VALUES (%s, %s, %s, %s)
    """
    result = execute_query(
        query,
        (session_id, data.get('name', ''), data.get('phone', ''), data.get('email', ''))
    )

    if not result:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Failed to create session'})
        }

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({
            'sessionId': session_id,
            'customerInfo': data
        })
    }

def get_session_orders(session_id):
    """Get all orders for a specific session"""
    query = """
        SELECT o.*, s.customer_name, s.phone_number
        FROM orders o
        JOIN sessions s ON o.session_id = s.session_id
        WHERE o.session_id = %s
        ORDER BY o.created_at DESC
    """
    orders = execute_query(query, (session_id,), fetch=True) or []

    for order in orders:
        item_query = """
            SELECT oi.*, m.item_name
            FROM order_items oi
            JOIN menu_items m ON oi.item_id = m.id
            WHERE oi.order_id = %s
        """
        order['items'] = execute_query(item_query, (order['id'],), fetch=True) or []

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'orders': orders})
    }

def get_conversation(session_id):
    """Get conversation history for a session"""
    query = """
        SELECT * FROM conversation_history
        WHERE session_id = %s
        ORDER BY created_at ASC
    """
    messages = execute_query(query, (session_id,), fetch=True) or []

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'messages': messages})
    }

# Vercel serverless function entry point
class handler_class(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def do_GET(self):
        # Parse path and query
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_string = parsed_url.query
        query_params = parse_qs(query_string) if query_string else {}

        # Create request object
        class Request:
            def __init__(self, method, path, headers, body=None, query=None):
                self.method = method
                self.path = path
                self.headers = headers
                self.body = body
                self.query = query

        request = Request('GET', path, dict(self.headers), query=query_params)
        response = handler(request)

        self.send_response(response['statusCode'])
        for key, value in response.get('headers', {}).items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(response['body'].encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else None

        # Parse path
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        # Create request object
        class Request:
            def __init__(self, method, path, headers, body):
                self.method = method
                self.path = path
                self.headers = headers
                self.body = body
                self.query = None

        class Body:
            def __init__(self, content):
                self.content = content

            def read(self):
                return self.content

        request = Request('POST', path, dict(self.headers), Body(body))
        response = handler(request)

        self.send_response(response['statusCode'])
        for key, value in response.get('headers', {}).items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(response['body'].encode('utf-8'))

    def do_PUT(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else None

        # Parse path
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        # Create request object
        class Request:
            def __init__(self, method, path, headers, body):
                self.method = method
                self.path = path
                self.headers = headers
                self.body = body
                self.query = None

        class Body:
            def __init__(self, content):
                self.content = content

            def read(self):
                return self.content

        request = Request('PUT', path, dict(self.headers), Body(body))
        response = handler(request)

        self.send_response(response['statusCode'])
        for key, value in response.get('headers', {}).items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(response['body'].encode('utf-8'))
