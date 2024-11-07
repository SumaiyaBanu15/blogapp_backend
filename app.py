from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for frontend requests from http://localhost:5173
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

def get_db():
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    return conn

# Drop and recreate the posts table
def init_db():
    db = get_db()
    db.execute('''
        DROP TABLE IF EXISTS posts
    ''')
    db.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            image TEXT,  -- Column for image URL
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    db.commit()

# GET route to fetch posts
@app.route('/api/posts', methods=['GET'])
def get_posts():
    try:
        db = get_db()
        posts = db.execute('SELECT * FROM posts ORDER BY created DESC').fetchall()
        return jsonify([dict(post) for post in posts]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# POST route to create a new post
@app.route('/api/posts', methods=['POST'])
def create_post():
    try:
        if not request.json or 'title' not in request.json or 'content' not in request.json:
            return jsonify({'error': 'Title and content are required'}), 400

        title = request.json['title']
        content = request.json['content']
        image = request.json.get('image', '')  # Capture image URL from request, empty if not provided

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO posts (title, content, image) VALUES (?, ?, ?)',  # Include image in insert
            (title, content, image)
        )
        db.commit()

        return jsonify({'message': 'Post created successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    # Delete The Post
@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    try:
        db = get_db()
        db.execute('DELETE FROM posts WHERE id = ?', (id,))
        db.commit()
        return jsonify({'message': 'Post deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Edit the Post
@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    try:
        if not request.json or 'title' not in request.json or 'content' not in request.json:
            return jsonify({'error': 'Title and content are required'}), 400
        
        title = request.json['title']
        content = request.json['content']

        db = get_db()
        db.execute(
            'UPDATE posts SET title = ?, content = ? WHERE id = ?',
            (title, content, id)
        )
        db.commit()

        return jsonify({'message': 'Post updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Call the function when the app starts
if __name__ == '__main__':
    init_db()  # Initialize the database by recreating the table
    app.run(debug=True)
