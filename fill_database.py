#!bin/python
from sqlalchemy import create_engine, text

engine = create_engine('mysql://task2_exordium:task2_exordium@localhost/task2_exordium')

def create_table():
    with engine.connect() as connection:
        connection.execute(text('DROP TABLE IF EXISTS task2_exordium'))
        print('DROP table => done')
        connection.execute(text('''CREATE TABLE task2_exordium (id INT NOT NULL AUTO_INCREMENT, timestamp TIMESTAMP NOT NULL DEFAULT 0, PRIMARY KEY (id))'''))
        print('CREATE table => done')

def insert_rows():
    with engine.connect() as connection:
        total = 0
        for i in range(0,864000,40):
            connection.execute(text('INSERT INTO task2_exordium (timestamp) VALUES (CURRENT_TIMESTAMP - INTERVAL :interval SECOND)'), {'interval': i})
            total += 1
        print('INSERT INTO table => done')
        print('Successfully inserted %d rows' % total)

def main():
    create_table()
    insert_rows()

if __name__ == '__main__':
    main()