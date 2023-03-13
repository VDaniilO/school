import schedule
import time
import requests
from bs4 import BeautifulSoup
import psycopg2

def parse_tasks():
    url = 'https://codeforces.com/problemset?order=BY_SOLVED_DESC'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    tasks = []
    for row in soup.find_all('tr')[1:]:
        columns = row.find_all('td')
        task = {
            'title': columns[0].text.strip(),
            'link': f"https://codeforces.com{columns[0].find('a')['href']}",
            'difficulty': int(columns[2].text.strip()),
            'topics': [tag.text.strip() for tag in columns[1].find_all('span')],
            'solved_count': int(columns[3].text.strip().replace(',', ''))
        }
        tasks.append(task)

    conn = psycopg2.connect(host="localhost", database="mydatabase", user="myusername", password="mypassword")
    cur = conn.cursor()

    for task in tasks:
        cur.execute("""
            INSERT INTO tasks (title, link, difficulty, topics, solved_count)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (link) DO NOTHING
        """, (task['title'], task['link'], task['difficulty'], task['topics'], task['solved_count']))
    conn.commit()

    cur.close()
    conn.close()

# start parse every 1 hour
schedule.every(1).hours.do(parse_tasks)

while True:
    schedule.run_pending()
    time.sleep(1)