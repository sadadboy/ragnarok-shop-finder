import os
import sys

class Config:
    SECRET_KEY = 'hard-to-guess-string'
    
    # 기본 PostgreSQL 연결 설정
    try:
        # PostgreSQL 연결 시도
        SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@127.0.0.1:5432/ragnarok_db'
        import psycopg2
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="admin",
            host="127.0.0.1",
            port="5432"
        )
        conn.close()
        print("PostgreSQL 연결 성공! PostgreSQL 데이터베이스를 사용합니다.")
    except Exception as e:
        # PostgreSQL 연결 실패 시 SQLite로 대체
        print(f"PostgreSQL 연결 실패: {e}")
        print("SQLite 데이터베이스로 대체합니다.")
        basedir = os.path.abspath(os.path.dirname(__file__))
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'ragnarok.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 디버그 모드
    DEBUG = True