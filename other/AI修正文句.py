import requests
import json
from datetime import datetime


def query_ollama(default_prompt, user_question):
    # 組合預設prompt和使用者提問
    full_prompt = f"{default_prompt}\n\n{user_question}"
    
    # 準備請求數據
    data = {
        "model": "llava",  # 使用你想要的模型名稱  #llava gemma2
        "prompt": full_prompt,
        "stream": False
    }
    
    # 發送POST請求到Ollama
    response = requests.post('http://localhost:11434/api/generate', json=data)
    
    if response.status_code == 200:
        result = response.json()
        return result['response']
    else:
        return f"錯誤: {response.status_code} - {response.text}"

def write_to_file(content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

# 使用範例

#user_question = "Python中如何創建一個列表？"
default_prompt = "用繁體中文修正以下句子的語句和錯字，並不要改變句子"
user_question="""許多人喜歡華小錢買刮刮樂，西望能一圓發財夢。
大陸一名男子近日前往彩券行買刮刮樂試手氣，
連續刮了許多張都槓龜，剩下的一張被女電員隨手刮開後卻中了大獎，
苦主傻眼的表情全被監視器錄下，畫面曝光後立刻引起網友熱議。"""

result = query_ollama(default_prompt, "以下為輸入文字{"+user_question+"}")

print(result)




# 生成包含時間戳的文件名
timestamp = datetime.now().strftime("%H%M%S")
filename = f"ollama_response_{timestamp}.txt"
# 將結果寫入文件
write_to_file(result, filename)
print(f"回答已寫入文件: {filename}")
