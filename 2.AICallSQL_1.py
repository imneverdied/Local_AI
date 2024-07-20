import requests
import json
from datetime import datetime
import sqlite3
import re

def query_ollama(default_prompt, user_question):
    full_prompt = f"{default_prompt}\n\n{user_question}"
    
    data = {
        "model": "gemma2",
        "prompt": full_prompt,
        "stream": False
    }
    
    response = requests.post('http://localhost:11434/api/generate', json=data)
    
    if response.status_code == 200:
        result = response.json()
        return result['response']
    else:
        return f"錯誤: {response.status_code} - {response.text}"

def extract_sql_query(response):
    # 使用正則表達式提取 SQL 查詢
    sql_match = re.search(r'```sql\s*(.*?)\s*```', response, re.DOTALL)
    if sql_match:
        return sql_match.group(1).strip()
    else:
        # 如果沒有找到 SQL 代碼塊，返回原始響應
        return response.strip()

def execute_sql_query(query):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        return column_names, results
    except sqlite3.Error as e:
        return None, f"SQLite error: {e}"
    finally:
        conn.close()

def write_to_file(content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

# 使用範例
default_prompt = "你是一個有幫助的SQL指令助手。請生成SQL指令來查詢books表。該表包含以下列：id, title, author, year, isbn。請只返回SQL查詢，不要包含任何其他解釋或標記。"
user_question = "幫我查詢年份在1950年以前的書單"

# 生成SQL查詢
ollama_response = query_ollama(default_prompt, user_question)
sql_query = extract_sql_query(ollama_response)

print("生成的SQL查詢:")
print(sql_query)

# 執行SQL查詢
column_names, results = execute_sql_query(sql_query)

# 生成包含時間戳的文件名
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"query_results_{timestamp}.txt"

# 準備寫入文件的內容
output_content = f"SQL Query:\n{sql_query}\n\nResults:\n"
if column_names:
    output_content += "\t".join(column_names) + "\n"
    for row in results:
        output_content += "\t".join(map(str, row)) + "\n"
else:
    output_content += str(results)  # 如果有錯誤，這裡會寫入錯誤信息

# 將結果寫入文件
write_to_file(output_content, filename)

print(f"\n查詢結果已寫入文件: {filename}")