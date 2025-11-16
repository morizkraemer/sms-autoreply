from psycopg import Connection


def create_tables(connection: Connection):
    with connection.cursor() as cursor:
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




