import requests
from bs4 import BeautifulSoup
import time

# base_url = "https://example-blog.com/page/{}"

# https://mercurychong.blogspot.com/2022/12/
# 我这里下载某年某月的文章，分页后又更多文章的不再下载
# base_url = "https://example-blog.com/page/{}"
base_url = "https://mercurychong.blogspot.com/2022/{}"

# 下载 21年 1月 到 25年5月的文章  2021/1  ~ 2025/5
for  year in range(2024, 2025):  # 假设有 5 年  
    for month in range(1, 13):  # 假设每年有 12 个月
        time.sleep(1)  # 避免请求过于频繁
        # 格式化月份
        month_str = f"{month:02d}"  # 确保月份是两位数
        url = f"https://mercurychong.blogspot.com/{year}/{month_str}/"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')

        articles = soup.select('h3 a')  # 根据具体网站结构调整

        for article in articles:
            link = article['href']
            article_res = requests.get(link)
            article_soup = BeautifulSoup(article_res.text, 'html.parser')
            title = article_soup.find('h3').text
            content = article_soup.find('div', class_='post-body').get_text(separator='\n')
            # print(f"Title: {title}\nContent: {content[:100]}...\n") 

            # with open(f"file/book/水星熊/{year}-{month_str}.txt", "a", encoding="utf-8") as f:
            with open(f"file/books/水星熊.txt", "a", encoding="utf-8") as f:
                f.write(f"{title}\n{content}\n---\n")
# for page in range(1, 13):  # 假设有 12 个月
#     time.sleep(1)  # 避免请求过于频繁
#     # 格式化月份
#     page_str = f"{page:02d}"  # 确保月份是两位数
#     url = base_url.format(page_str)
#     res = requests.get(url)
#     soup = BeautifulSoup(res.text, 'html.parser')

#     # print(f"Fetching articles from {url}")
#     # print(soup.find('h3',class_='post-title entry-title').text)
#     articles = soup.select('h3 a')  # 根据具体网站结构调整
#     # print(f"Found {len(articles)} articles on page {page}")
#     # print("hello----")

#     for article in articles:
#         link = article['href']
#         article_res = requests.get(link)
#         article_soup = BeautifulSoup(article_res.text, 'html.parser')
#         title = article_soup.find('h3').text
#         content = article_soup.find('div', class_='post-body').text
#         print(f"Title: {title}\nContent: {content[:100]}...\n")

        # with open(f"file/book/水星熊/{title}.txt", "w", encoding="utf-8") as f:
        #     f.write(content)