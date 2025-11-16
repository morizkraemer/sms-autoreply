import psycopg
import pprint
import logging
import sys

conn_string = "host = 'db' dbname='gsm' user='admin' password='passwd'"
class Database:
    def __init__(self, conn_string):

        logging.info(f"Connecting db to {conn_string}")
        self.conn = psycopg.connect(conn_string)
        logging.info("DB connected")
        self.init()
        pass


    def init(self):
        with self.conn.cursor() as cursor:
            try:

                cursor.execute("""
                               SET TIME ZONE 'Europe/Berlin';
                               """)
                self.conn.commit()
            except psycopg.Error as e:
                logging.info(e)
            except Exception as e:
                logging.info(e)
        logging.info("Set timezone")

    def create_tables(self):
        with self.conn.cursor() as cursor:
            try:
                cursor.execute(
                                   """
                                   CREATE TABLE IF NOT EXISTS messages (
                                           id serial PRIMARY KEY
                                           number VARCHAR(255)
                                           recieved_text VARCHAR(255)
                                           replied BOOLEAN
                                           reply_text VARCHAR(255)
                                           date TIMESTAMP WITH TIME ZONE
                                       )

                                    CREATE TABLE IF NOT EXISTS reply_texts (
                                        id serial PRIMARY KEY
                                        text VARCHAR(255)
                                        is_selected BOOLEAN
                                        )
                                   """
                               )
                self.conn.commit()
            except psycopg.Error as e:
                logging.info(e)
            except Exception as e:
                logging.info(e)
        logging.info("Created Tables")


    def retrieve_tables(self):
        with self.conn.cursor() as cursor:
            cursor.execute(
                            """

                            SELECT TABLE_NAME
                            FROM INFORMATION_SCHEMA.TABLES
                            WHERE TABLE_SCHEMA = 'public';
                            """
                           )
            response = cursor.fetchall()
            pprint.pprint(response)
            sys.stdout.flush()



