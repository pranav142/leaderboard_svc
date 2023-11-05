from flask import Flask, request, jsonify
import mysql.connector
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

class Database:
    def __enter__(self):
        self.conn = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

def get_leaderboard(cursor):
    query = "SELECT username, streak_count FROM Users ORDER BY streak_count DESC"
    cursor.execute(query)
    result = cursor.fetchall()
    
    leaderboard_data = [{'username': row[0], 'streak_count': row[1]} for row in result]
    return leaderboard_data

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    try:
        with Database() as cursor:
            leaderboard_data = get_leaderboard(cursor)
            return jsonify(leaderboard_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

