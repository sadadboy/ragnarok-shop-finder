from flask import Blueprint, jsonify, request
from app.models import db, Shop, Item

main = Blueprint('main', __name__)

@main.route('/api/shops', methods=['GET'])
def get_shops():
    shops = Shop.query.all()
    return jsonify([shop.to_dict() for shop in shops])

@main.route('/api/items', methods=['GET'])
def get_items():
    # 아이템 이름으로 검색
    name = request.args.get('name', '')
    items = Item.query.filter(Item.name.ilike(f'%{name}%')).all()
    
    return jsonify([item.to_dict() for item in items])

@main.route('/api/items/<int:id>', methods=['GET'])
def get_item(id):
    item = Item.query.get_or_404(id)
    return jsonify(item.to_dict())

@main.route('/api/shops/<int:id>', methods=['GET'])
def get_shop(id):
    shop = Shop.query.get_or_404(id)
    shop_data = shop.to_dict()
    shop_data['items'] = [item.to_dict() for item in shop.items]
    return jsonify(shop_data)