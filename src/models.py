from sqlalchemy import Column, String, Integer
from sqlalchemy.sql import exists
from typing import List
from database import Base, s

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(String, primary_key=True)
    link = Column(String)
    name = Column(String)
    topic = Column(String, index=True)
    difficulty = Column(Integer, index=True)
    solved = Column(Integer)

    def __init__(self, id: str, link: str, name: str, topic: str, difficulty: int, solved: int):
        self.id = id
        self.link = link
        self.name = name
        self.topic = topic
        self.difficulty = difficulty
        self.solved = solved

    def __repr__(self) -> str:
        return f'Задача №{self.id} - {self.name} на {self.topic} тему\nСложность {self.difficulty}, решено {self.solved}\n' \
               f'{self.link}'

    def create(self):
        s.add(self)
        s.commit()
        return self

    @classmethod
    def is_exists(cls, param) -> bool:
        if s.query(exists().where(cls.id == param)).scalar():
            return True
        return False

    @classmethod
    def filter_difficulty_data(cls, param: int) -> List[str]:
        topics = []
        for topic in s.query(cls).filter_by(difficulty=param).all():
            if topic.topic not in topics:
                topics.append(topic.topic)
        return topics

    @classmethod
    def filter_diff_topic_data(cls, diff: str, topic: str):
        return s.query(cls).filter_by(difficulty=diff).filter_by(topic=topic).all()[:10]
