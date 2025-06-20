import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import random
import logging
from config.config import GOOGLE_EMAIL, GOOGLE_PASSWORD, BASE_URLS

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Hàm đăng nhập bằng tài khoản Google
def login_to_wsj_with_google(driver, google_email, google_password):
    login_url = "https://accounts.wsj.com/login"
    try:
        driver.get(login_url)
        google_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "signin-google-btn"))
        )
        google_button.click()
        WebDriverWait(driver, 15).until(EC.number_of_windows_to_be(2))
        driver.switch_to.window(driver.window_handles[1])
        email_field = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        )
        email_field.clear()
        email_field.send_keys(google_email)
        driver.find_element(By.ID, "identifierNext").click()
        password_field = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "Passwd"))
        )
        password_field.clear()
        password_field.send_keys(google_password)
        driver.find_element(By.ID, "passwordNext").click()
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "totpPin"))
            )
            logging.warning("Yêu cầu mã 2FA. Vui lòng nhập mã thủ công.")
            return False
        except TimeoutException:
            pass
        WebDriverWait(driver, 15).until(EC.number_of_windows_to_be(1))
        driver.switch_to.window(driver.window_handles[0])
        WebDriverWait(driver, 15).until(EC.url_contains("wsj.com"))
        logging.info("Đăng nhập bằng Google thành công")
        return True
    except Exception as e:
        logging.error(f"Lỗi đăng nhập bằng Google: {e}")
        return False

# Hàm crawl bài báo từ một URL
def scrape_article(url, driver):
    try:
        driver.get(url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "lxml")
        headline_elem = soup.select_one("h1.WSJTheme--headline--7VCzo7Ay")
        headline = headline_elem.get_text().strip() if headline_elem else "N/A"
        date_elem = soup.select_one("time")
        pub_date = date_elem.get_text().strip() if date_elem else "N/A"
        content_elems = soup.select("div.article-content p")
        content = " ".join([elem.get_text().strip() for elem in content_elems]) if content_elems else "N/A"
        return {
            "tieude": headline,
            "ngay_dang": pub_date,
            "noi_dung": content,
            "url": url
        }
    except Exception as e:
        logging.error(f"Lỗi khi crawl bài báo {url}: {e}")
        return None

# Hàm crawl bài báo ngẫu nhiên
def crawl_wsj_articles(section="home", max_articles=5):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(options=options)
    try:
        if not login_to_wsj_with_google(driver, GOOGLE_EMAIL, GOOGLE_PASSWORD):
            return []
        base_url = BASE_URLS.get(section, "https://www.wsj.com/")
        articles_data = []
        driver.get(base_url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "lxml")
        article_links = soup.select("article a")
        article_urls = [link["href"] for link in article_links if link.get("href") and "wsj.com/articles" in link["href"]]
        if len(article_urls) > max_articles:
            article_urls = random.sample(article_urls, max_articles)
        for url in article_urls:
            logging.info(f"Đang crawl bài báo: {url}")
            article_data = scrape_article(url, driver)
            if article_data:
                articles_data.append(article_data)
            time.sleep(3)
        return articles_data
    finally:
        driver.quit()

# Hàm chính
def main():
    section = "stocks"
    max_articles = 5
    articles_data = crawl_wsj_articles(section, max_articles)
    if articles_data:
        # Lưu vào file CSV
        df = pd.DataFrame(articles_data)
        df.to_csv("data/wsj_articles_full.csv", index=False, encoding="utf-8")
        logging.info("Dữ liệu bài báo đã được lưu vào data/wsj_articles_full.csv")
        # Lưu nội dung vào file text
        with open("data/wsj_articles_content.txt", "w", encoding="utf-8") as f:
            for article in articles_data:
                f.write(article["noi_dung"] + "\n\n")
        logging.info("Nội dung bài báo đã được lưu vào data/wsj_articles_content.txt")
    else:
        logging.warning("Không crawl được bài báo nào")

if __name__ == "__main__":
    main()