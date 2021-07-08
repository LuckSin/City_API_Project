import psycopg2


CONN = psycopg2.connect(
                        host='127.0.0.1', port='5432', database='test', user='root', password='root')
CURSOR = CONN.cursor()
API_KEYS = 'a2354620-f8b1-44a6-b922-2d1555463719'
VERSION_YANDEX = '1.x/?apikey='
