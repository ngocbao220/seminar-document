import pandas as pd
from src.read_articles import read_articles_content
import requests
import json
import logging

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Truy vấn đối thoại
STOCK_PROMPT = """
Giả sử bạn là một nhà phân tích tài chính cao cấp. Xin vui lòng đọc kỹ tin tức sau từ Wall Street Journal: 
"{content}"
Theo nội dung của tin tức, nếu bạn đã tư vấn mua cổ phiếu nào, hãy viết 'CÓ' và liệt kê 5 tên cổ phiếu NYSE hoặc Nasdaq cùng với mã cổ phiếu mà bạn đề xuất. Nếu bạn chỉ trả lời 'KHÔNG', xin vui lòng giải thích ngắn gọn lý do.
"""

INDUSTRY_PROMPT = """
Giả sử bạn là một nhà phân tích tài chính cao cấp. Xin vui lòng đọc kỹ tin tức chính sách sau: 
"{content}"
Dựa trên nội dung của tin tức chính sách và tham chiếu đến tiêu chuẩn phân loại SIC hai chữ số, nếu bạn đã được các ngành nghề được đề xuất, hãy viết 'CÓ' và liệt kê mã danh mục của ngành nghề được đề xuất. Nếu bạn vừa trả lời 'KHÔNG', vui lòng giải thích ngắn gọn lý do.
"""

# Hàm gọi API AI (giả lập, cần thay thế bằng API thực tế)
def call_ai_api(prompt):
    # Thay thế bằng API thực tế (ví dụ: OpenAI API hoặc xAI API)
    # Đây là giả lập kết quả
    logging.warning("API AI chưa được triển khai. Trả về kết quả mẫu.")
    return {
        "response": "CÓ",
        "details": [
            {"stock": "First Solar", "ticker": "FSLR"},
            {"stock": "SunPower Corporation", "ticker": "SPWR"},
            {"stock": "Enphase Energy Inc.", "ticker": "ENPH"},
            {"stock": "SolarEdge Technologies", "ticker": "SEDG"},
            {"stock": "Sunrun Inc.", "ticker": "RUN"}
        ],
        "reason": ""
    }

# Hàm phân tích bài báo và tạo khuyến nghị
def analyze_articles():
    articles = read_articles_content("data/wsj_articles_content.txt")
    full_articles = pd.read_csv("data/wsj_articles_full.csv")
    recommendations = []
    
    for i, content in enumerate(articles):
        article_url = full_articles.iloc[i]["url"]
        
        # Phân tích cổ phiếu
        stock_prompt = STOCK_PROMPT.format(content=content)
        stock_result = call_ai_api(stock_prompt)
        recommendations.append({
            "article_url": article_url,
            "recommendation_type": "stock",
            "recommendation": stock_result["response"],
            "details": json.dumps(stock_result["details"]),
            "reason": stock_result["reason"]
        })
        
        # Phân tích ngành
        industry_prompt = INDUSTRY_PROMPT.format(content=content)
        industry_result = call_ai_api(industry_prompt)
        recommendations.append({
            "article_url": article_url,
            "recommendation_type": "industry",
            "recommendation": industry_result["response"],
            "details": json.dumps(industry_result["details"]),
            "reason": industry_result["reason"]
        })
    
    # Lưu khuyến nghị
    df = pd.DataFrame(recommendations)
    df.to_csv("data/recommendations.csv", index=False, encoding="utf-8")
    logging.info("Khuyến nghị đã được lưu vào data/recommendations.csv")

if __name__ == "__main__":
    analyze_articles()