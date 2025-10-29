import traceback
import pandas as pd
from flask import Flask, jsonify, render_template
import os

app = Flask(__name__)

DATA_FILENAME = 'books_scraped.csv' 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, DATA_FILENAME)

df_books = None

RATING_MAP = {
    'One': 1, 
    'Two': 2, 
    'Three': 3, 
    'Four': 4, 
    'Five': 5
}

def load_data():
    """Tải dữ liệu từ file CSV và tiền xử lý cơ bản."""
    global df_books
    print(f"Bắt đầu tải dữ liệu từ {DATA_FILE}...")
    
    try:
        df_books = pd.read_csv(DATA_FILE, encoding='utf-8') 
        
        df_books = df_books.rename(columns={
            'Title': 'title',
            'Star_rating': 'rating_str', 
            'Price': 'price',
            'Stock': 'stock_status',
            'Quantity': 'quantity'
        })
        
        df_books['author'] = df_books['Book_category']
        
        df_books['rating'] = df_books['rating_str'].map(RATING_MAP)
        
        df_books['price'] = df_books['price'].replace({r'[^\d\.]': ''}, regex=True).astype(float)
        
        df_books = df_books.fillna({'author': 'N/A', 'rating': 0})
        
        df_books = df_books[['title', 'author', 'rating', 'price', 'stock_status', 'quantity']].copy()
        
        print(f"Tải dữ liệu thành công! {df_books.shape[0]} đầu sách được tải.")
        
    except FileNotFoundError:
        print(f"LỖI: KHÔNG TÌM THẤY TỆP DỮ LIỆU. Đã cố gắng truy cập tại: {DATA_FILE}")
        print("Vui lòng đảm bảo file books_scraped.csv nằm cùng thư mục với app.py.")
        df_books = pd.DataFrame()
        
    except Exception as e:
        print(f"LỖỖI XỬ LÝ DỮ LIỆU: {type(e).__name__} - {e}")
        traceback.print_exc() 
        df_books = pd.DataFrame()

    return df_books

@app.route('/')
def index():
    """Route chính: Hiển thị giao diện web (dự kiến là index.html)."""
    return render_template('index.html')

@app.route('/api/books', methods=['GET'])
def get_all_books():
    """Trả về toàn bộ danh sách sách dưới dạng JSON."""
    global df_books
    
    if df_books is None or df_books.empty:
        load_data()
        if df_books.empty:
            return jsonify({"error": "Dữ liệu chưa được tải hoặc không có sẵn. Vui lòng kiểm tra log backend."}), 500

    books_list = df_books.to_dict('records')
    return jsonify(books_list)

@app.route('/api/authors', methods=['GET'])
def get_authors():
    """Trả về danh sách duy nhất các Tác giả (hiện là Book_category) dưới dạng JSON."""
    global df_books
    
    if df_books is None or df_books.empty:
        load_data() 
        if df_books.empty:
            return jsonify([]), 200

    authors = df_books['author'].dropna().unique().tolist()
    authors.sort() 
    return jsonify(authors)

load_data() 
if __name__ == '__main__':
    app.run(debug=True)
