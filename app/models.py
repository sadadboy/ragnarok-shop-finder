from app import db
from datetime import datetime

class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vendor_name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    items = db.relationship('Item', backref='shop', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'vendor_name': self.vendor_name,
            'location': self.location,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'items_count': len(self.items)
        }

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, default=1)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    item_icon_url = db.Column(db.String(255), nullable=True)  # 아이템 아이콘 URL
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity,
            'shop_id': self.shop_id,
            'created_at': self.created_at.isoformat(),
            'vendor_name': self.shop.vendor_name,
            'item_icon_url': self.item_icon_url  # 아이콘 URL 추가
        }

class EnchantedItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    vendor_name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    server = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    item_type = db.Column(db.String(10), nullable=False)  # 의상 부위 (상의, 중의, 하의, 걸칠것, 상하, 상중, 중하, 상중하)
    enchant_keyword = db.Column(db.String(10), nullable=False)
    slots = db.Column(db.Text, nullable=True)  # 슬롯 정보 (콤마로 구분된 목록)
    random_options = db.Column(db.Text, nullable=True)  # 랜덤 옵션 정보 (콤마로 구분된 목록)
    is_costume = db.Column(db.Boolean, default=True)  # 의상 아이템 여부
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    item_icon_url = db.Column(db.String(255), nullable=True)  # 아이템 아이콘 URL
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'vendor_name': self.vendor_name,
            'location': self.location,
            'server': self.server,
            'timestamp': self.timestamp.isoformat(),
            'item_type': self.item_type,
            'enchant_keyword': self.enchant_keyword,
            'slots': self.slots,
            'random_options': self.random_options,
            'is_costume': self.is_costume,
            'item_icon_url': self.item_icon_url  # 아이콘 URL 추가
        }