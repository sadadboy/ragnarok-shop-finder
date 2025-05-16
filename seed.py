from app import create_app, db
from app.models import Shop, Item
import random

app = create_app()

def seed_database():
    with app.app_context():
        # 기존 데이터 삭제
        db.drop_all()
        db.create_all()
        
        # 샘플 노점 생성
        locations = ['Prontera', 'Payon', 'Morroc', 'Geffen', 'Alberta']
        items = [
            {'name': '포링 카드', 'price_range': (500000, 1000000)},
            {'name': '해적 스켈레톤 카드', 'price_range': (800000, 1500000)},
            {'name': '+7 양손검', 'price_range': (200000, 400000)},
            {'name': '민첩의 열매', 'price_range': (10000, 20000)},
            {'name': '바포메트 주니어 카드', 'price_range': (2000000, 3500000)},
            {'name': '혈정수 10개', 'price_range': (5000, 10000)},
            {'name': '에메랄드', 'price_range': (30000, 50000)},
            {'name': '황금 해머', 'price_range': (100000, 200000)},
        ]
        
        # 노점 20개 생성
        for i in range(1, 21):
            shop = Shop(
                vendor_name=f'Vendor{i}',
                location=random.choice(locations)
            )
            db.session.add(shop)
            
            # 각 노점마다 1-5개 아이템 추가
            for _ in range(random.randint(1, 5)):
                item_data = random.choice(items)
                price = random.randint(item_data['price_range'][0], item_data['price_range'][1])
                item = Item(
                    name=item_data['name'],
                    price=price,
                    quantity=random.randint(1, 3),
                    shop=shop
                )
                db.session.add(item)
        
        db.session.commit()
        print("샘플 데이터 생성 완료!")

if __name__ == '__main__':
    seed_database()