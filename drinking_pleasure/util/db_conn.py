import pymysql
from DBUtils.PooledDB import PooledDB
from drinking_pleasure.my_settings import MY_DBCONFIG, DATABASE


def db_conn(func):
    """
    decorator function for DB connection
    """

    def wrapper(*args, **kwargs):
        try:
            db_conn = MAZLE_DB.connection()
            cursor = db_conn.cursor(pymysql.cursors.DictCursor)

            sp_result = func(*args, **kwargs, cursor=cursor)

            return True, sp_result
        except Exception as e:
            print(f'SP Error, SP: {func.__name__}(), Error Message: {e}')

            return False, None
        finally:
            cursor.close()
            db_conn.close()

    wrapper.__name__ = func.__name__
    return wrapper


try:
    MAZLE_DB = PooledDB(
        creator=pymysql,
        mincached=DATABASE['mincached'],
        maxconnections=DATABASE['maxconnections'],
        blocking=True,
        host=MY_DBCONFIG['host'],
        port=MY_DBCONFIG['port'],
        user=MY_DBCONFIG['user'],
        password=MY_DBCONFIG['password'],
        db=MY_DBCONFIG['database'],
        charset='utf8mb4',
        use_unicode=True,
        autocommit=True,
        connect_timeout=DATABASE['connect_timeout'],
        ping=DATABASE['ping'],
    )
except Exception as e:
    msg = '[Emergency Error] cannot connect to MySQL - \
           [host: {}, db: {}, error: {}]'.format(
            MY_DBCONFIG['host'], MY_DBCONFIG['database'], e)
    print(msg)
