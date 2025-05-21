from flask import Blueprint, jsonify, request
from app.models import db, Shop, EnchantedItem
from app.crawlers.ragnarok_crawler import RagnarokCrawler
from datetime import datetime, timedelta
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

main = Blueprint('main', __name__)
crawler = RagnarokCrawler()

@main.route('/api/shops', methods=['GET'])
def get_shops():
    shops = Shop.query.all()
    return jsonify([shop.to_dict() for shop in shops])

@main.route('/api/shops/<int:id>', methods=['GET'])
def get_shop(id):
    shop = Shop.query.get_or_404(id)
    shop_data = shop.to_dict()
    shop_data['items'] = [item.to_dict() for item in shop.items]
    return jsonify(shop_data)

@main.route('/api/search', methods=['GET'])
def search_items():
    """실시간 검색 엔드포인트"""
    keywords = request.args.get('q', '')
    server_id = request.args.get('server', '')
    item_type = request.args.get('type', '')
    order = request.args.get('order', 'ASC')  # 기본값을 ASC(오름차순)으로 변경
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)  # 페이지당 항목 수 (기본 20개)
    
    logger.info(f"Realtime search request: keywords='{keywords}', server_id='{server_id}', type='{item_type}', order='{order}', page={page}, per_page={per_page}")
    
    if not keywords:
        logger.warning("Search request rejected: No keywords provided")
        return jsonify({"error": "검색어가 필요합니다"}), 400
    
    # 크롤러 호출 - 페이지네이션 정보 포함된 결과 반환
    search_result = crawler.search_items(keywords, server_id, item_type, order, page)
    
    # 에러 응답 처리
    if isinstance(search_result, dict) and "error" in search_result:
        logger.error(f"Search error: {search_result['error']}")
        return jsonify(search_result), 500
    
    # 새 크롤러 결과 형식 처리
    if isinstance(search_result, dict) and "items" in search_result and "pagination" in search_result:
        items = search_result["items"]
        pagination = search_result["pagination"]
        
        # 페이지네이션 처리
        total_items = pagination.get('total_items', len(items))
        total_pages = pagination.get('total_pages', 1)
        current_page = pagination.get('current_page', page)
        
        logger.info(f"Search successful: {total_items} items found, showing page {current_page} of {total_pages}")
        
        # 결과 반환 - 페이지네이션 정보도 포함
        return jsonify({
            'items': items,
            'total': total_items,
            'pages': total_pages,
            'current_page': current_page,
            'per_page': per_page,
            'has_next': pagination.get('has_next', False),
            'has_prev': pagination.get('has_prev', False)
        })
    else:
        # 이전 버전 호환성 유지
        items = search_result if isinstance(search_result, list) else []
        
        # 페이징 처리
        total_items = len(items)
        total_pages = (total_items + per_page - 1) // per_page  # 올림 나눗셈
        
        # 현재 페이지에 해당하는 아이템만 추출
        start_idx = (page - 1) * per_page
        end_idx = min(start_idx + per_page, total_items)
        
        current_page_items = items[start_idx:end_idx]
        
        logger.info(f"Search successful: {total_items} items found, showing page {page} of {total_pages}")
        
        # 결과 반환
        return jsonify({
            'items': current_page_items,
            'total': total_items,
            'pages': total_pages,
            'current_page': page,
            'per_page': per_page,
            'has_next': page < total_pages,
            'has_prev': page > 1
        })

@main.route('/api/enchanted', methods=['GET'])
def get_enchanted_items():
    """저장된 인챈트 아이템 조회 엔드포인트"""
    keywords = request.args.get('q', '')
    server_id = request.args.get('server', '')
    costume_type = request.args.get('costume_type', '')  # 의상 부위별 필터링
    enchant_keyword = request.args.get('enchant', '')    # 인챈트 키워드별 필터링
    order = request.args.get('order', 'price_desc')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # 최근 24시간 이내의 데이터만 조회
    cutoff_time = datetime.utcnow() - timedelta(days=1)
    
    query = EnchantedItem.query.filter(EnchantedItem.created_at >= cutoff_time)
    
    # 이제 is_costume=True인 아이템만 필터링 (의상 아이템만)
    query = query.filter(EnchantedItem.is_costume == True)
    
    if keywords:
        query = query.filter(EnchantedItem.name.ilike(f'%{keywords}%'))
    
    if server_id:
        query = query.filter(EnchantedItem.server == server_id)
    
    if costume_type:
        # 의상 타입 필터링 (상의, 중의, 하의, 걸칠것, 복합 타입)
        query = query.filter(EnchantedItem.item_type == costume_type)
    
    if enchant_keyword:
        # 인챈트 키워드 필터링 (int+, str+, vit+ 등)
        query = query.filter(EnchantedItem.enchant_keyword.ilike(f'%{enchant_keyword}%'))
    
    # 정렬 조건 적용
    if order == 'price_desc':
        query = query.order_by(EnchantedItem.price.desc())
    elif order == 'price_asc':
        query = query.order_by(EnchantedItem.price.asc())
    elif order == 'time_desc':
        query = query.order_by(EnchantedItem.timestamp.desc())
    
    # 페이지네이션
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    items = pagination.items
    
    # 고유한 의상 타입 목록 가져오기
    costume_types = db.session.query(EnchantedItem.item_type).distinct().all()
    costume_types = [t[0] for t in costume_types if t[0]]
    
    # 고유한 인챈트 키워드 목록 가져오기
    enchant_keywords = db.session.query(EnchantedItem.enchant_keyword).distinct().all()
    enchant_keywords = [k[0] for k in enchant_keywords if k[0]]
    
    return jsonify({
        'items': [item.to_dict() for item in items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'has_next': page < pagination.pages,
        'has_prev': page > 1,
        'costume_types': costume_types,
        'enchant_keywords': enchant_keywords
    })

@main.route('/api/admin/crawl-enchanted', methods=['POST'])
def trigger_enchanted_crawl():
    """관리자용: 인챈트 의상 아이템 크롤링 트리거"""
    # 실제 구현에서는 관리자 인증 필요
    try:
        # 기존 데이터 삭제 (1일 이상 지난 데이터)
        cutoff_time = datetime.utcnow() - timedelta(days=1)
        EnchantedItem.query.filter(EnchantedItem.created_at < cutoff_time).delete()
        
        # 새 데이터 크롤링
        search_result = crawler.crawl_enchanted_items()
        
        # 결과 형식 처리
        if isinstance(search_result, dict) and "error" in search_result:
            return jsonify({
                'success': False,
                'message': f'Crawling failed: {search_result["error"]}'
            }), 500
        
        # 다양한 형식 지원 (dict 또는 list)
        items = []
        if isinstance(search_result, dict) and "items" in search_result:
            items = search_result["items"]
        elif isinstance(search_result, list):
            items = search_result
            
        # 의상 아이템 개수 카운트
        costume_types = db.session.query(EnchantedItem.item_type, db.func.count(EnchantedItem.id)).group_by(EnchantedItem.item_type).all()
        costume_count_info = {costume_type: count for costume_type, count in costume_types}
        
        return jsonify({
            'success': True,
            'message': f'Successfully crawled {len(items)} enchanted costume items',
            'costume_types': costume_count_info
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Crawling failed: {str(e)}'
        }), 500