import pandas as pd
import logging

# Thiết lập logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Hàm nhập đánh giá từ nhà phân tích
def get_evaluator_input(recommendation, article_url, rec_type):
    print(f"\nĐánh giá khuyến nghị cho bài báo: {article_url}")
    print(f"Loại khuyến nghị: {rec_type}")
    print(f"Khuyến nghị: {recommendation['recommendation']}")
    print(f"Chi tiết: {recommendation['details']}")
    print(f"Lý do (nếu KHÔNG): {recommendation['reason']}")
    print("Tiêu chí: 1. Tính liên quan, 2. Độ hợp lý, 3. Cơ hội đầu tư")
    result = input("Nhập đánh giá (hợp lý/không rõ ràng/không liên quan): ").strip().lower()
    return result

# Hàm đánh giá khuyến nghị
def evaluate_recommendations():
    try:
        df = pd.read_csv("data/recommendations.csv")
    except FileNotFoundError:
        logging.error("Không tìm thấy file recommendations.csv")
        return
    
    evaluations = []
    for _, row in df.iterrows():
        eval_1 = get_evaluator_input(row, row["article_url"], row["recommendation_type"])
        eval_2 = get_evaluator_input(row, row["article_url"], row["recommendation_type"])
        
        if eval_1 == eval_2:
            final_result = eval_1
        else:
            print("Hai đánh giá khác nhau, cần nhà phân tích thứ ba.")
            eval_3 = get_evaluator_input(row, row["article_url"], row["recommendation_type"])
            results = [eval_1, eval_2, eval_3]
            if results.count(eval_1) >= 2:
                final_result = eval_1
            elif results.count(eval_2) >= 2:
                final_result = eval_2
            else:
                final_result = "bỏ qua (khác nhau hoàn toàn)"
        
        evaluations.append({
            "article_url": row["article_url"],
            "recommendation_type": row["recommendation_type"],
            "recommendation": row["recommendation"],
            "details": row["details"],
            "reason": row["reason"],
            "evaluator_1": eval_1,
            "evaluator_2": eval_2,
            "evaluator_3": eval_3 if eval_1 != eval_2 else "",
            "final_result": final_result
        })
    
    # Lưu kết quả đánh giá
    df_eval = pd.DataFrame(evaluations)
    df_eval.to_csv("data/evaluated_recommendations.csv", index=False, encoding="utf-8")
    logging.info("Kết quả đánh giá đã được lưu vào data/evaluated_recommendations.csv")

if __name__ == "__main__":
    evaluate_recommendations()