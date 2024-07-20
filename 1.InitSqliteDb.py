import sqlite3

# 連接到SQLite數據庫（如果不存在，則創建）
conn = sqlite3.connect('books.db')
cursor = conn.cursor()

# 創建books表
cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year INTEGER,
    isbn TEXT
)
''')

# 插入10筆示例數據
sample_books = [
    ('The Great Gatsby', 'F. Scott Fitzgerald', 1925, '9780743273565'),
    ('To Kill a Mockingbird', 'Harper Lee', 1960, '9780446310789'),
    ('1984', 'George Orwell', 1949, '9780451524935'),
    ('Pride and Prejudice', 'Jane Austen', 1813, '9780141439518'),
    ('The Catcher in the Rye', 'J.D. Salinger', 1951, '9780316769174'),
    ('One Hundred Years of Solitude', 'Gabriel García Márquez', 1967, '9780060883287'),
    ('The Hobbit', 'J.R.R. Tolkien', 1937, '9780261102217'),
    ('The Da Vinci Code', 'Dan Brown', 2003, '9780307474278'),
    ('The Alchemist', 'Paulo Coelho', 1988, '9780062315007'),
    ('Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 1997, '9780747532743')
]

# 刪除舊數據（如果存在）
cursor.execute('DELETE FROM books')

# 插入新數據
cursor.executemany('INSERT INTO books (title, author, year, isbn) VALUES (?, ?, ?, ?)', sample_books)

# 提交更改並關閉連接
conn.commit()
conn.close()

print("資料庫已更新，並插入了10筆示例數據。")

# 顯示插入的數據
conn = sqlite3.connect('books.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM books')
print("\n已插入的書籍資料：")
for row in cursor.fetchall():
    print(row)
conn.close()