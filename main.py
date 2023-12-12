import sqlalchemy
import json
import os
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Book, Shop, Stock, Sale

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
dbname = os.getenv("DBname")
DSN = f'postgresql://{USERNAME}:{PASSWORD}@localhost:5432/{dbname}'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json', encoding='utf-8') as data_file:
    data = json.load(data_file)
    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))

publisher_id = input('Введите id издателя чтобы получить\n'
                     'его имя, название книги, магазина и\n'
                     'доступное количество книг на данный момента: ')
for p in session.query(Publisher, Book, Shop, Stock).select_from(Publisher).\
        join(Book, Stock, Shop).filter(Publisher.id == publisher_id).all():
    print(p)

session.commit()
session.close()