// 메인 JavaScript 파일
document.addEventListener('DOMContentLoaded', function() {
    console.log('라그나로크 노점 검색 웹사이트가 로드되었습니다.');
    
    // 검색 폼 기능 향상
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const input = this.querySelector('input');
            if (input.value.trim() === '') {
                e.preventDefault();
                alert('검색어를 입력해주세요.');
            }
        });
    }
    
    // 가격 포맷팅
    const prices = document.querySelectorAll('.item-price');
    prices.forEach(price => {
        const priceText = price.textContent;
        const priceValue = parseInt(priceText);
        if (!isNaN(priceValue)) {
            price.textContent = priceValue.toLocaleString() + ' 제니';
        }
    });
});