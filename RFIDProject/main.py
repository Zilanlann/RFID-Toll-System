from db_connections import *
from link_serial import *

if __name__ == '__main__':
    # ser = init_serial()
    init_table()
    delete_all()
    cursor.close()
    db.close()
