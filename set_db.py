import sqlite3
import os

database_filename = 'my_database.db'

def create_db():
    database_filename = 'my_database.db'

    # データベースファイルを作成（存在しない場合）
    conn = sqlite3.connect(database_filename)
    conn.close()

def create_tables():
    conn = sqlite3.connect(database_filename)
    cursor = conn.cursor()

    # match_info テーブルを作成
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS match_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            victory_or_lose TEXT,
            left_team TEXT,
            right_team TEXT
        )
    ''')

    conn.commit()
    conn.close()

def main():
    # dbファイルが存在しなかったらcreate_db()とcreate_tables()を実行する
    if not os.path.exists(database_filename):
        create_db()
        create_tables()
    else:
        print('dbファイルが存在します。')
    
if __name__ == '__main__':
    main()