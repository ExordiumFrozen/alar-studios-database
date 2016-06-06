#!bin/python
from time import sleep
from sqlalchemy import create_engine, text

engine = create_engine('mysql://task2_exordium:task2_exordium@localhost/task2_exordium')

def get_ids():
    ids_to_delete = None
    with engine.connect() as connection:
        ids_to_delete = connection.execute(text('SELECT id from task2_exordium WHERE timestamp <= CURRENT_TIMESTAMP - INTERVAL 5 DAY'))
    return ids_to_delete


def grouper_by_offset(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


def main():
    ids_to_delete = get_ids()
    ids_to_delete_list = []
    for row in ids_to_delete:
        ids_to_delete_list.append(row[0])

    iteration = 1
    with engine.connect() as connection:
        for group in grouper_by_offset(ids_to_delete_list, 100):
            query_ids = ''
            for id_to_delete in group:
                query_ids += str(id_to_delete) + ','
            query_ids = query_ids[:-1]
            query_string = 'DELETE FROM task2_exordium WHERE id in (' + query_ids + ')'
            print('Processing iteration ' + str(iteration))
            connection.execute(text(query_string))
            sleep(0.2)
            iteration += 1


if __name__ == '__main__':
    main()