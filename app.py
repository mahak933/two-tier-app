from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-this')

# Database configuration
DB_CONFIG = {
    'host': os.environ.get('MYSQL_HOST', 'localhost'),
    'port': os.environ.get('MYSQL_PORT', '3306'),
    'user': os.environ.get('MYSQL_USER', 'root'),
    'password': os.environ.get('MYSQL_PASSWORD', ''),
    'database': os.environ.get('MYSQL_DB', 'todo_db')
}

def get_db_connection():
    """Create and return database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def init_db():
    """Initialize database and create tables if they don't exist"""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS todos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    task VARCHAR(255) NOT NULL,
                    status ENUM('pending', 'completed') DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            connection.commit()
            print("Database initialized successfully!")
        except Error as e:
            print(f"Error initializing database: {e}")
        finally:
            cursor.close()
            connection.close()

@app.route('/')
def index():
    """Display all todos"""
    connection = get_db_connection()
    todos = []
    
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM todos ORDER BY created_at DESC")
            todos = cursor.fetchall()
        except Error as e:
            flash(f'Error fetching todos: {str(e)}', 'error')
        finally:
            cursor.close()
            connection.close()
    else:
        flash('Database connection failed', 'error')
    
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    """Add a new todo"""
    task = request.form.get('task')
    
    if not task:
        flash('Task cannot be empty!', 'error')
        return redirect(url_for('index'))
    
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO todos (task) VALUES (%s)", (task,))
            connection.commit()
            flash('Todo added successfully!', 'success')
        except Error as e:
            flash(f'Error adding todo: {str(e)}', 'error')
        finally:
            cursor.close()
            connection.close()
    else:
        flash('Database connection failed', 'error')
    
    return redirect(url_for('index'))

@app.route('/complete/<int:todo_id>')
def complete_todo(todo_id):
    """Mark a todo as completed"""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE todos SET status = 'completed' WHERE id = %s", (todo_id,))
            connection.commit()
            flash('Todo marked as completed!', 'success')
        except Error as e:
            flash(f'Error updating todo: {str(e)}', 'error')
        finally:
            cursor.close()
            connection.close()
    else:
        flash('Database connection failed', 'error')
    
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    """Delete a todo"""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
            connection.commit()
            flash('Todo deleted successfully!', 'success')
        except Error as e:
            flash(f'Error deleting todo: {str(e)}', 'error')
        finally:
            cursor.close()
            connection.close()
    else:
        flash('Database connection failed', 'error')
    
    return redirect(url_for('index'))

@app.route('/health')
def health():
    """Health check endpoint"""
    connection = get_db_connection()
    if connection:
        connection.close()
        return {'status': 'healthy', 'database': 'connected'}, 200
    return {'status': 'unhealthy', 'database': 'disconnected'}, 503

if __name__ == '__main__':
    init_db()  # Initialize database on startup
    app.run(host='0.0.0.0', port=5000, debug=True)

