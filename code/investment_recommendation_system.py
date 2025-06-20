import openai
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import json
import time
import logging
from typing import List, Dict, Tuple, Optional
import re

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InvestmentRecommendationSystem:
    def __init__(self, openai_api_key: str):
        """
        Khởi tạo hệ thống với API key của OpenAI
        """
        self.client = openai.OpenAI(api_key=openai_api_key)
        self.sic_codes = self._load_sic_codes()
        
    def _load_sic_codes(self) -> Dict[str, str]:
        """
        Tải danh sách mã SIC (Standard Industrial Classification)
        """
        # Đây là một mẫu các mã SIC phổ biến
        sic_codes = {
            "01": "Agricultural Production - Crops",
            "02": "Agricultural Production - Livestock",
            "10": "Metal Mining",
            "13": "Oil and Gas Extraction",
            "15": "Building Construction",
            "20": "Food and Kindred Products",
            "22": "Textile Mill Products",
            "23": "Apparel and Other Textile Products",
            "26": "Paper and Allied Products",
            "28": "Chemicals and Allied Products",
            "29": "Petroleum and Coal Products",
            "33": "Primary Metal Industries",
            "34": "Fabricated Metal Products",
            "35": "Industrial Machinery and Equipment",
            "36": "Electronic and Other Electric Equipment",
            "37": "Transportation Equipment",
            "38": "Instruments and Related Products",
            "39": "Miscellaneous Manufacturing Industries",
            "40": "Railroad Transportation",
            "44": "Water Transportation",
            "45": "Transportation by Air",
            "48": "Communications",
            "49": "Electric, Gas, and Sanitary Services",
            "50": "Wholesale Trade - Durable Goods",
            "51": "Wholesale Trade - Nondurable Goods",
            "52": "Building Materials and Garden Supplies",
            "53": "General Merchandise Stores",
            "54": "Food Stores",
            "55": "Automotive Dealers and Service Stations",
            "56": "Apparel and Accessory Stores",
            "57": "Furniture and Home Furnishings Stores",
            "58": "Eating and Drinking Places",
            "59": "Miscellaneous Retail",
            "60": "Depository Institutions",
            "61": "Nondepository Institutions",
            "62": "Security and Commodity Brokers",
            "63": "Insurance Carriers",
            "64": "Insurance Agents and Brokers",
            "65": "Real Estate",
            "67": "Holding and Other Investment Offices",
            "70": "Hotels and Other Lodging Places",
            "72": "Personal Services",
            "73": "Business Services",
            "75": "Auto Repair, Services, and Parking",
            "76": "Miscellaneous Repair Services",
            "78": "Motion Pictures",
            "79": "Amusement and Recreation Services",
            "80": "Health Services",
            "81": "Legal Services",
            "82": "Educational Services",
            "83": "Social Services",
            "84": "Museums, Botanical, Zoological Gardens",
            "86": "Membership Organizations",
            "87": "Engineering and Management Services",
            "88": "Private Households",
            "89": "Services, Not Elsewhere Classified"
        }
        return sic_codes
    
    def get_stock_recommendations(self, news_content: str, temperature: float = 1.0) -> Dict:
        """
        Lấy khuyến nghị cổ phiếu từ ChatGPT dựa trên tin tức
        """
        prompt = f"""
        Giả sử bạn là một nhà phân tích tài chính cao cấp. Xin vui lòng đọc kỹ tin tức sau từ Wall Street Journal. 
        
        Tin tức: {news_content}
        
        Theo nội dung của tin tức, nếu bạn có tư vấn mua cổ phiếu nào, hãy viết 'CÓ' và liệt kê 5 tên cổ phiếu NYSE hoặc Nasdaq cùng với mã cổ phiếu mà bạn đề xuất, kèm theo lý do ngắn gọn cho mỗi cổ phiếu.
        
        Nếu bạn trả lời 'KHÔNG', xin vui lòng giải thích ngắn gọn lý do.
        
        Định dạng trả lời:
        - Nếu CÓ: "CÓ\n1. Tên công ty (Mã): Lý do\n2. ..."
        - Nếu KHÔNG: "KHÔNG\nLý do: ..."
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=1000
            )
            
            return self._parse_stock_response(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"Lỗi khi gọi OpenAI API: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_sector_recommendations(self, policy_news: str, temperature: float = 1.0) -> Dict:
        """
        Lấy khuyến nghị ngành từ ChatGPT dựa trên tin tức chính sách
        """
        sic_info = "\n".join([f"{code}: {name}" for code, name in self.sic_codes.items()])
        
        prompt = f"""
        Giả sử bạn là một nhà phân tích tài chính cao cấp. Xin vui lòng đọc kỹ tin tức chính sách sau.
        
        Tin tức chính sách: {policy_news}
        
        Dựa trên nội dung của tin tức chính sách và tham chiếu đến tiêu chuẩn phân loại SIC hai chữ số dưới đây:
        {sic_info}
        
        Nếu bạn có các ngành nghề được đề xuất, hãy viết 'CÓ' và liệt kê mã danh mục của ngành nghề được đề xuất kèm theo lý do.
        
        Nếu bạn trả lời 'KHÔNG', vui lòng giải thích ngắn gọn lý do.
        
        Định dạng trả lời:
        - Nếu CÓ: "CÓ\n1. Mã SIC: Tên ngành - Lý do\n2. ..."
        - Nếu KHÔNG: "KHÔNG\nLý do: ..."
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=1000
            )
            
            return self._parse_sector_response(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"Lỗi khi gọi OpenAI API: {e}")
            return {"status": "error", "message": str(e)}
    
    def _parse_stock_response(self, response: str) -> Dict:
        """
        Phân tích phản hồi khuyến nghị cổ phiếu
        """
        result = {"status": "unknown", "recommendations": [], "reason": ""}
        
        if response.strip().upper().startswith("CÓ"):
            result["status"] = "yes"
            lines = response.split('\n')[1:]  # Bỏ dòng "CÓ"
            
            for line in lines:
                if line.strip():
                    # Tìm mã cổ phiếu trong ngoặc đơn
                    match = re.search(r'([A-Z]{1,5})\):', line)
                    if match:
                        symbol = match.group(1)
                        reason = line.split(':', 1)[1].strip() if ':' in line else ""
                        company_name = line.split('(')[0].strip().split('.', 1)[1].strip() if '.' in line else ""
                        
                        result["recommendations"].append({
                            "symbol": symbol,
                            "company_name": company_name,
                            "reason": reason
                        })
        
        elif response.strip().upper().startswith("KHÔNG"):
            result["status"] = "no"
            if "Lý do:" in response:
                result["reason"] = response.split("Lý do:")[1].strip()
        
        return result
    
    def _parse_sector_response(self, response: str) -> Dict:
        """
        Phân tích phản hồi khuyến nghị ngành
        """
        result = {"status": "unknown", "recommendations": [], "reason": ""}
        
        if response.strip().upper().startswith("CÓ"):
            result["status"] = "yes"
            lines = response.split('\n')[1:]  # Bỏ dòng "CÓ"
            
            for line in lines:
                if line.strip():
                    # Tìm mã SIC
                    match = re.search(r'(\d{2}):', line)
                    if match:
                        sic_code = match.group(1)
                        content = line.split(':', 1)[1].strip() if ':' in line else ""
                        
                        result["recommendations"].append({
                            "sic_code": sic_code,
                            "sector_name": self.sic_codes.get(sic_code, "Unknown"),
                            "reason": content
                        })
        
        elif response.strip().upper().startswith("KHÔNG"):
            result["status"] = "no"
            if "Lý do:" in response:
                result["reason"] = response.split("Lý do:")[1].strip()
        
        return result
    
    def validate_stock_recommendations(self, recommendations: List[Dict]) -> Dict:
        """
        Kiểm tra tính hợp lệ của các khuyến nghị cổ phiếu
        """
        validation_results = []
        
        for rec in recommendations:
            symbol = rec["symbol"]
            validation = {
                "symbol": symbol,
                "exists": False,
                "current_price": None,
                "market_cap": None,
                "sector": None,
                "error": None
            }
            
            try:
                # Lấy thông tin cổ phiếu từ Yahoo Finance
                stock = yf.Ticker(symbol)
                info = stock.info
                hist = stock.history(period="1d")
                
                if not hist.empty:
                    validation["exists"] = True
                    validation["current_price"] = hist['Close'].iloc[-1]
                    validation["market_cap"] = info.get('marketCap', None)
                    validation["sector"] = info.get('sector', None)
                    validation["industry"] = info.get('industry', None)
                else:
                    validation["error"] = "Không tìm thấy dữ liệu giá"
                    
            except Exception as e:
                validation["error"] = str(e)
            
            validation_results.append(validation)
            time.sleep(0.1)  # Tránh rate limiting
        
        return {
            "total_recommendations": len(recommendations),
            "valid_stocks": len([v for v in validation_results if v["exists"]]),
            "validation_details": validation_results
        }
    
    def backtest_recommendations(self, recommendations: List[Dict], days_forward: int = 30) -> Dict:
        """
        Kiểm tra hiệu suất của các khuyến nghị trong quá khứ
        """
        results = []
        
        for rec in recommendations:
            symbol = rec["symbol"]
            
            try:
                # Lấy dữ liệu giá trong khoảng thời gian kiểm tra
                stock = yf.Ticker(symbol)
                end_date = datetime.now()
                start_date = end_date - timedelta(days=days_forward + 30)
                
                hist = stock.history(start=start_date, end=end_date)
                
                if len(hist) >= days_forward:
                    # Giả sử mua vào ngày đầu tiên có dữ liệu
                    buy_price = hist['Close'].iloc[0]
                    # Bán sau days_forward ngày
                    sell_price = hist['Close'].iloc[days_forward] if days_forward < len(hist) else hist['Close'].iloc[-1]
                    
                    returns = (sell_price - buy_price) / buy_price * 100
                    
                    results.append({
                        "symbol": symbol,
                        "buy_price": buy_price,
                        "sell_price": sell_price,
                        "returns_pct": returns,
                        "days_held": min(days_forward, len(hist) - 1)
                    })
                    
            except Exception as e:
                logger.error(f"Lỗi khi backtest {symbol}: {e}")
                results.append({
                    "symbol": symbol,
                    "error": str(e)
                })
        
        # Tính toán thống kê tổng thể
        valid_results = [r for r in results if "returns_pct" in r]
        
        if valid_results:
            avg_return = np.mean([r["returns_pct"] for r in valid_results])
            win_rate = len([r for r in valid_results if r["returns_pct"] > 0]) / len(valid_results)
            
            return {
                "total_stocks": len(recommendations),
                "tested_stocks": len(valid_results),
                "average_return": avg_return,
                "win_rate": win_rate,
                "individual_results": results
            }
        else:
            return {
                "total_stocks": len(recommendations),
                "tested_stocks": 0,
                "error": "Không thể kiểm tra hiệu suất cho bất kỳ cổ phiếu nào"
            }
    
    def generate_report(self, news_content: str, recommendations: Dict, 
                       validation: Dict, backtest: Dict = None) -> str:
        """
        Tạo báo cáo tổng hợp
        """
        report = f"""
=== BÁO CÁO PHÂN TÍCH KHUYẾN NGHỊ ĐẦU TƯ ===

Thời gian tạo báo cáo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

1. TIN TỨC PHÂN TÍCH:
{news_content[:500]}...

2. KẾT QUẢ KHUYẾN NGHỊ:
Trạng thái: {recommendations.get('status', 'Unknown')}
Số lượng khuyến nghị: {len(recommendations.get('recommendations', []))}

"""
        
        if recommendations.get('status') == 'yes':
            report += "3. CHI TIẾT KHUYẾN NGHỊ:\n"
            for i, rec in enumerate(recommendations['recommendations'], 1):
                report += f"{i}. {rec.get('company_name', 'N/A')} ({rec.get('symbol', 'N/A')})\n"
                report += f"   Lý do: {rec.get('reason', 'N/A')}\n"
        
        report += f"""
4. KIỂM TRA TÍNH HỢP LỆ:
- Tổng số khuyến nghị: {validation['total_recommendations']}
- Số cổ phiếu hợp lệ: {validation['valid_stocks']}
- Tỷ lệ hợp lệ: {validation['valid_stocks']/validation['total_recommendations']*100:.1f}%

"""
        
        if backtest:
            report += f"""
5. KIỂM TRA HIỆU SUẤT:
- Tổng số cổ phiếu kiểm tra: {backtest['total_stocks']}
- Số cổ phiếu có dữ liệu: {backtest['tested_stocks']}
- Lợi nhuận trung bình: {backtest.get('average_return', 0):.2f}%
- Tỷ lệ thắng: {backtest.get('win_rate', 0)*100:.1f}%
"""
        
        return report

# Ví dụ sử dụng
# def main():
#     # Khởi tạo hệ thống
#     api_key = "open-ai-api-key"  # Thay thế bằng API key thực
#     system = InvestmentRecommendationSystem(api_key)
    
#     # Tin tức mẫu
#     sample_news = """
#     Biden sẽ Hoãn Thuế Nhập Khẩu về Năng Lượng Mặt Trời. 
#     Quyết định này sẽ có tác động tích cực đến các công ty năng lượng tái tạo 
#     và có thể làm giảm chi phí lắp đặt tấm pin mặt trời cho người tiêu dùng.
#     Các nhà sản xuất tấm pin mặt trời trong nước được kỳ vọng sẽ hưởng lợi 
#     từ chính sách này.
#     """
    
#     # Lấy khuyến nghị
#     print("Đang lấy khuyến nghị cổ phiếu...")
#     recommendations = system.get_stock_recommendations(sample_news)
#     print(f"Kết quả: {recommendations}")
    
#     # Kiểm tra tính hợp lệ
#     if recommendations.get('status') == 'yes':
#         print("\nĐang kiểm tra tính hợp lệ...")
#         validation = system.validate_stock_recommendations(recommendations['recommendations'])
#         print(f"Kết quả kiểm tra: {validation}")
        
#         # Kiểm tra hiệu suất (nếu có dữ liệu)
#         print("\nĐang kiểm tra hiệu suất...")
#         backtest = system.backtest_recommendations(recommendations['recommendations'])
#         print(f"Kết quả backtest: {backtest}")
        
#         # Tạo báo cáo
#         report = system.generate_report(sample_news, recommendations, validation, backtest)
#         print("\n" + report)

