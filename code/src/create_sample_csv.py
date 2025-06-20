
import pandas as pd

# Dữ liệu mẫu cho 5 bài báo
sample_articles = [
    {
        "tieude": "Cổ phiếu công nghệ tăng mạnh sau báo cáo thu nhập quý 2",
        "ngay_dang": "June 18, 2025",
        "noi_dung": "Các công ty công nghệ lớn như Apple và Microsoft đã báo cáo kết quả kinh doanh vượt kỳ vọng, dẫn đến sự tăng trưởng mạnh mẽ trên thị trường chứng khoán. Các nhà đầu tư đang lạc quan về triển vọng của ngành công nghệ trong bối cảnh phục hồi kinh tế. Tuy nhiên, một số chuyên gia cảnh báo về rủi ro lạm phát.",
        "url": "https://www.wsj.com/articles/tech-stocks-surge-20250618"
    },
    {
        "tieude": "Cục Dự trữ Liên bang cân nhắc tăng lãi suất",
        "ngay_dang": "June 17, 2025",
        "noi_dung": "Cục Dự trữ Liên bang (Fed) đang thảo luận về khả năng tăng lãi suất lần đầu tiên trong năm nay, nhằm kiểm soát lạm phát. Các nhà kinh tế dự đoán rằng động thái này có thể ảnh hưởng đến thị trường chứng khoán và chi phí vay vốn của doanh nghiệp.",
        "url": "https://www.wsj.com/articles/fed-rate-hike-20250617"
    },
    {
        "tieude": "Tesla mở rộng nhà máy tại Trung Quốc",
        "ngay_dang": "June 16, 2025",
        "noi_dung": "Tesla thông báo kế hoạch mở rộng nhà máy Gigafactory tại Thượng Hải để đáp ứng nhu cầu ngày càng tăng về xe điện. Động thái này được kỳ vọng sẽ củng cố vị thế của Tesla tại thị trường lớn nhất thế giới.",
        "url": "https://www.wsj.com/articles/tesla-china-expansion-20250616"
    },
    {
        "tieude": "Thị trường dầu mỏ biến động do căng thẳng địa chính trị",
        "ngay_dang": "June 15, 2025",
        "noi_dung": "Giá dầu thô tăng vọt sau các báo cáo về căng thẳng ở Trung Đông, làm dấy lên lo ngại về nguồn cung. Các nhà phân tích cho rằng giá dầu có thể tiếp tục tăng nếu tình hình không được giải quyết.",
        "url": "https://www.wsj.com/articles/oil-market-geopolitical-tensions-20250615"
    },
    {
        "tieude": "Amazon đầu tư mạnh vào trí tuệ nhân tạo",
        "ngay_dang": "June 14, 2025",
        "noi_dung": "Amazon công bố khoản đầu tư 2 tỷ USD vào các dự án trí tuệ nhân tạo, tập trung vào cải thiện trợ lý ảo Alexa và các dịch vụ đám mây. Các nhà đầu tư kỳ vọng khoản đầu tư này sẽ thúc đẩy tăng trưởng dài hạn của công ty.",
        "url": "https://www.wsj.com/articles/amazon-ai-investment-20250614"
    }
]

# Tạo DataFrame và lưu vào file CSV
def create_sample_csv():
    df = pd.DataFrame(sample_articles)
    df.to_csv("data/wsj_articles_sample.csv", index=False, encoding="utf-8")
    print("Đã tạo file mẫu data/wsj_articles_sample.csv")

if __name__ == "__main__":
    create_sample_csv()