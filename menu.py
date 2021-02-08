import json
import psycopg2

#db 연결
conn_string = "host='localhost' dbname = 'restaurant' user = 'postgres' password = '1029'"
conn = psycopg2.connect(conn_string)
cur = conn.cursor()

# cur.execute("CREATE TABLE restaurant (place_id VARCHAR(10), place_filename VARCHAR(30), place_name VARCHAR(100), place_x FLOAT, place_y FLOAT, place_address VARCHAR(100), place_tel VARCHAR(20));")
# conn.commit()

# cur.execute("CREATE TABLE menu (place_id VARCHAR(10), menu_price_kr VARCHAR(100));")
# conn.commit()

file_path = "./menu.json"

with open(file_path, 'r', encoding='UTF8') as json_file:
    json_data = json.load(json_file)

    for image_no in json_data:
        try:
            cur.execute("INSERT into restaurant (place_id, place_filename, place_name, place_x, place_y, place_address, place_tel) values (%s, %s, %s, %s, %s, %s, %s);",(
                    json_data[image_no]['file_attributes']['rid'], json_data[image_no]['filename'], json_data[image_no]['file_attributes']['title'],
                    json_data[image_no]['file_attributes']['latitude'],json_data[image_no]['file_attributes']['longitude'],
                    json_data[image_no]['file_attributes']['addr'], json_data[image_no]['file_attributes']['tel']))
            conn.commit()
        except:
            pass
        try:
            for menu in json_data[image_no]['regions']:
                cur.execute("INSERT into menu (place_id, menu_price_kr) values (%s, %s);", (
                json_data[image_no]['file_attributes']['rid'], menu['region_attributes']['annotation_kr'].replace('\n', ' ').replace('\\', '')))
                conn.commit()
        except:
            pass
            # print(json_data[image_no]['file_attributes']['rid'])

cur.close()
conn.close()
