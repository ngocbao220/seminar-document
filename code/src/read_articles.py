import logging

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Hàm đọc nội dung bài báo
def read_articles_content(file_path="data/wsj_articles_content.txt"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            articles = [article.strip() for article in content.split("\n\n") if article.strip()]
        return articles
    except FileNotFoundError:
        logging.error(f"Không tìm thấy file {file_path}")
        return []
    except Exception as e:
        logging.error(f"Lỗi khi đọc file: {e}")
        return []

# Hàm chính
def main():
    articles_content = read_articles_content()
    if articles_content:
        logging.info(f"Đã đọc {len(articles_content)} bài báo:")
        for i, article in enumerate(articles_content, 1):
            logging.info(f"Bài báo {i}: {article[:100]}..." if len(article) > 100 else article)
    else:
        logging.warning("Không có bài báo nào được đọc")

if __name__ == "__main__":
    main()