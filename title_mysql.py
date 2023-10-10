import requests
from bs4 import BeautifulSoup
import mysql.connector
from datetime import datetime

# 指定目标网页的URL
url = 'https://bbs.hupu.com/all-gambia'

# 发送HTTP请求获取网页内容
response = requests.get(url)

# 检查响应状态码，确保请求成功
if response.status_code == 200:
    # 使用Beautiful Soup解析网页内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 获取当前日期作为表格名称
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 设置数据库连接参数
    db_config = {
        'host': '192.168.19.82',
        'user': 'root',
        'password': 'gcloud123',
        'database': 'hup'
    }

    # 连接到MySQL数据库
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # 查找所有具有class属性为"list-item-wrap"的<div>标签
        divs_with_class_1 = soup.find_all('div', class_='list-item-wrap')

        # 构建查询语句，检查是否已存在相同的数据
        check_query = "SELECT COUNT(*) FROM title WHERE text = %s AND href = %s"

        # 遍历这些<div>标签
        for div_tag in divs_with_class_1:
            # 在每个<div>标签下查找具有class属性为"t-title"的<span>元素
            span_tag = div_tag.find('span', class_='t-title')

            # 检查是否找到了<span>元素
            if span_tag:
                # 提取<span>元素的文本内容
                span_text = span_tag.text

                # 查找<div>标签下的<a>标签
                a_tag = div_tag.find('a')

                # 检查是否找到了<a>标签
                if a_tag:
                    # 提取<a>标签的href属性值
                    href_attr = 'https://bbs.hupu.com' + a_tag.get('href')

                    # 使用查询语句检查是否已存在相同数据
                    cursor.execute(check_query, (span_text, href_attr))
                    result = cursor.fetchone()

                    # 如果查询结果为0（即没有相同数据），则插入数据
                    if result[0] == 0:
                        # 将数据插入到数据库表中
                        insert_query = "INSERT INTO title (text, href, date_added) VALUES (%s, %s, %s)"
                        data = (span_text, href_attr, current_date)
                        cursor.execute(insert_query, data)
                        connection.commit()

        print(f'信息已写入数据库：{current_date}')

    except mysql.connector.Error as err:
        print(f'数据库错误：{err}')

    finally:
        # 关闭数据库连接
        cursor.close()
        connection.close()

else:
    print('请求失败，状态码：', response.status_code)

