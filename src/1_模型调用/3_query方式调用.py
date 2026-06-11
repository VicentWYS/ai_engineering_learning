import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")
base_url = os.getenv("DEEPSEEK_BASE_URL")

if not api_key or api_key == "your_api_key_here":
    raise ValueError("\n请先在.env文件中设置有效的DEEPSEEK_API_KEY\n")

if not base_url or base_url == "your_base_url_here":
    raise ValueError("\n请先在.env文件中设置有效的DEEPSEEK_API_KEY\n")


# 初始化OpenAI客户端
client = OpenAI(
    base_url=base_url,
    api_key=api_key
)

def query(user_prompt):
    try:
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[
                {"role": "user",
                 "content": user_prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"错误：{str(e)}"

if __name__ == "__main__":
    print(query("讲一个关于手机的简短笑话"))