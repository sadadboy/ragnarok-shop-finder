from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # CORS 설정 (React와의 통신용)
    CORS(app)
    
    # 데이터베이스 초기화
    db.init_app(app)
    
    # 라우트 등록
    from app.routes import main
    app.register_blueprint(main)
    
    return app