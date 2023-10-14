from db_connections import *
from link_serial import *

if __name__ == '__main__':
    # ser = init_serial()
    init_table()
    add_new_car("苏J99999", "FFFFFF")
    car_entry("FFFFFF")
    # sleep(10)
    car_exit("FFFFFF")
    delete_all()
    cursor.close()
    db.close()
