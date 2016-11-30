import psycopg2 as pg
import configparser

config = configparser.ConfigParser()
config.read('study.cfg')


def setup_db():
    try:
        connstring = "dbname=%s user=%s" % (config.get("postgresql", "dbname"), config.get("postgresql", "dbuser"))
        conn = pg.connect(connstring)
    except:
        print("I am unable to connect to the database")

    cur = conn.cursor()
    cur.execute("CREATE TABLE paper_pulls (id serial, data json);")
    conn.commit()
    print("successfully created table")

if __name__ == "__main__":
    setup_db()
