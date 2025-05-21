from app import create_app, db
from app.models import Shop, Item, EnchantedItem
from scheduler import setup_scheduler
import atexit
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = create_app()

# 애플리케이션 컨텍스트 내에서 스케줄러 설정
with app.app_context():
    scheduler = setup_scheduler(app)
    
    # 애플리케이션 종료 시 스케줄러도 종료
    atexit.register(lambda: scheduler.shutdown())

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'Shop': Shop, 
        'Item': Item, 
        'EnchantedItem': EnchantedItem
    }

if __name__ == '__main__':
    logger.info("라그나로크 노점 검색 서버 시작")
    app.run(debug=True)