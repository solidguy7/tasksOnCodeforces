import requests
from bs4 import BeautifulSoup
from asyncz.schedulers.asyncio import AsyncIOScheduler
from asyncz.triggers import IntervalTrigger
from models import Task

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0'
}

scheduler = AsyncIOScheduler()

difficulties = []

def generate_url_and_soup(page: int) -> BeautifulSoup:
    url = f'https://codeforces.com/problemset/page/{page}?order=BY_SOLVED_DESC'
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup

def count_pages() -> int:
    soup = generate_url_and_soup(page=1)
    number_pages = int(soup.find('div', class_='pagination').find('a', class_='arrow').find_previous('a').text.strip())
    return number_pages

@scheduler.scheduled_task(trigger=IntervalTrigger(hours=1))
def check_fresh_tasks():
    for page in range(1, count_pages() + 1):
        soup = generate_url_and_soup(page=page)
        rows = soup.find('table', class_='problems').find('tr')

        for row in range(100):
            try:
                rows = rows.find_next('tr')
                id = rows.find('a').text.strip()
                link = f"https://codeforces.com{rows.find('a').get('href')}"
                name = rows.find('a').find_next('a').text.strip()
                topics = rows.find_next('div',
                                    style='float: right; font-size: 1.1rem; padding-top: 1px; text-align: right;').text.strip().splitlines()
                topic = []
                for ind in range(len(topics)):
                    if ind == len(topics) - 1:
                        topic.append(topics[ind].strip())
                    else:
                        topic.append(topics[ind][:-1])
                if len(topic) != 1:
                    continue
                topic = ''.join(topic)
                difficulty = int(rows.find('span', class_='ProblemRating').text.strip())
                solved = int(rows.find(title='Participants solved the problem').text.strip()[1:])
                if not difficulty in difficulties:
                    difficulties.append(difficulty)
                if Task.is_exists(id):
                    continue
            except AttributeError:
                continue
            task = Task(id=id, link=link, name=name, topic=topic, difficulty=difficulty, solved=solved)
            task.create()

scheduler.start()
