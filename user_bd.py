from sqlalchemy import create_engine, Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

engine = create_engine("postgresql://dylvhcvruqtuvo:d685ee31d82bc085d821a2871bc274517c6234855f476781fa1d9ef66fe3dfb1@ec2-34-254-69-72.eu-west-1.compute.amazonaws.com:5432/dab8bbumauh2n4", echo=True, connect_args={'check_same_thread': False})

# базовый деклоративный класс
base = declarative_base()

Session = sessionmaker(engine)
session = Session()


class Statistics(base):
    __tablename__ = 'statistic'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    theme_id = Column(Integer, ForeignKey('word.id'))
    count = Column(Integer, default=0)

class User(base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_repetition = Column(DateTime) #последнее повторение
    theme_id = Column(String, default=1) # тема
    repeat_word = Column(Integer, default=5) # кол-во повторений слов
    last_word = Column(Integer) # последнее выученное слово
    test_count = Column(Integer, default=3) # количество вопросов в тесте
    words_list = relationship("Statistics")
    count_learn_word = Column(Integer, default=0) #кол-во выученных слов

    def refresh(self):
        session.add(self)
        session.commit()

class Word(base):
    __tablename__ = 'word'
    id = Column(Integer, primary_key=True, autoincrement=True)
    theme_id = Column(String, ForeignKey('theme.id'))
    word = Column(String)
    translation = Column(String)
    example = Column(String)

class Theme(base):
    __tablename__ = 'theme'
    id = Column(String, primary_key=True)
    words = relationship("Word")

    def add(self, word: Word):
        session.add(word)
        session.commit()


def init_user(id):
    user = session.query(User).get(id)
    if not user:
        user = User()
        user.id = id
        user.theme_id = "Crime"
        session.add(user)
        session.commit()
    return user


base.metadata.create_all(engine)
