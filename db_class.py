import psycopg2

class db:
    def __init__(self, conn):
        self.conn = conn

    def create_db(self, conn):
        with conn.cursor() as cur:
            cur.execute("""
                        CREATE TABLE IF NOT EXISTS clients(
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(30) NOT NULL,
                            surname VARCHAR(30) NOT NULL,
                            email VARCHAR(30) NOT NULL UNIQUE
                        );
                        """)
            cur.execute("""
                        CREATE TABLE IF NOT EXISTS phones(
                            id SERIAL PRIMARY KEY,
                            id_client INTEGER NOT NULL REFERENCES clients(id),
                            number VARCHAR(15) NOT NULL UNIQUE
                        );
                        """)
            conn.commit()

    def add_client(self, conn, first_name, last_name, email, phones=None):
        with conn.cursor() as cur:
            cur.execute("""
                    INSERT INTO clients(name, surname, email) VALUES(%s, %s, %s) RETURNING id; 
                    """, (first_name, last_name, email))
            id = cur.fetchone()
            if phones:
                for number in phones:
                    cur.execute("""
                                INSERT INTO phones(id_client, number) VALUES(%s, %s);
                                """, (id, number))
            conn.commit()

    def add_phone(self, conn, client_id, phone):
        with conn.cursor() as cur:
            cur.execute("""
                        INSERT INTO phones(id_client, number) VALUES(%s, %s);
                        """, (client_id, phone))
            conn.commit()

    def change_client(self, conn, client_id, first_name=None, last_name=None, email=None, phones=None):
        with conn.cursor() as cur:
            if first_name:
                if last_name:
                    if email:
                        cur.execute("""UPDATE clients SET first_name=%s surname=%s, email=%s WHERE id=%s;
                                    """, (first_name, last_name, email, client_id,))
                    else:
                        cur.execute("""UPDATE clients SET first_name=%s surname=%s WHERE id=%s;
                                    """, (first_name, last_name, client_id,))
                else:
                    if email:
                        cur.execute("""UPDATE clients SET first_name=%s email=%s WHERE id=%s;
                                    """, (first_name, email, client_id,))
                    else:
                        cur.execute("""UPDATE clients SET first_name=%s WHERE id=%s;
                                    """, (first_name, client_id,))
            else:
                if last_name:
                    if email:
                        cur.execute("""UPDATE clients SET surname=%s, email=%s WHERE id=%s;
                                    """, (last_name, email, client_id,))
                    else:
                        cur.execute("""UPDATE clients SET surname=%s WHERE id=%s;
                                    """, (last_name, client_id,))
                else:
                    if email:
                        cur.execute("""UPDATE clients SET email=%s WHERE id=%s;
                                   """, (email, client_id,))
            conn.commit()
            if phones:
                cur.execute("""
                            DELETE FROM phones WHERE id_client=%s;
                            """, (client_id,))
                for number in phones:
                    self.add_phone(conn, client_id, number)
            conn.commit()

    def delete_phone(self, conn, client_id, phone):
        with conn.cursor() as cur:
            cur.execute("""
                        DELETE FROM phones WHERE id_client=%s AND number=%s;
                        """, (client_id, phone))
            conn.commit()

    def delete_client(self, conn, client_id):
        with conn.cursor() as cur:
            cur.execute("""
                        DELETE FROM phones WHERE id_client=%s;
                        """, (client_id,))
            cur.execute("""
                        DELETE FROM clients WHERE id=%s;
                        """, (client_id,))
            conn.commit()

    def find_client(self, conn, first_name=None, last_name=None, email=None, phone=None):
        with conn.cursor() as cur:
            if first_name:
                if last_name:
                    if email:
                        if phone:
                            cur.execute("""
                                       SELECT * FROM clients c 
                                       JOIN phones p on c.id = p.id_client
                                       WHERE c.name=%s AND c.surname=%s AND c.email=%s AND p.number=%s
                                       """, (first_name, last_name, email, phone))
                        else:
                            cur.execute("""
                                       SELECT * FROM clients
                                       WHERE name=%s AND surname=%s AND email=%s
                                       """, (first_name, last_name, email))
                    else:
                        if phone:
                            cur.execute("""
                                       SELECT * FROM clients c 
                                       JOIN phones p on c.id = p.id_client
                                       WHERE c.name=%s AND c.surname=%s AND p.number=%s
                                       """, (first_name, last_name, phone))
                        else:
                            cur.execute("""
                                       SELECT * FROM clients
                                       WHERE name=%s AND surname=%s
                                       """, (first_name, last_name))
                else:
                    if email:
                        if phone:
                            cur.execute("""
                                       SELECT * FROM clients c 
                                       JOIN phones p on c.id = p.id_client
                                       WHERE c.name=%s AND c.email=%s AND p.number=%s
                                       """, (first_name, email, phone))
                        else:
                            cur.execute("""
                                       SELECT * FROM clients
                                       WHERE name=%s AND email=%s
                                       """, (first_name, email))
                    else:
                        if phone:
                            cur.execute("""
                                       SELECT * FROM clients c 
                                       JOIN phones p on c.id = p.id_client
                                       WHERE c.name=%s AND p.number=%s
                                       """, (first_name, phone))
                        else:
                            cur.execute("""
                                       SELECT * FROM clients
                                       WHERE name=%s 
                                       """, (first_name, ))
            else:
                if last_name:
                    if email:
                        if phone:
                            cur.execute("""
                                       SELECT * FROM clients c 
                                       JOIN phones p on c.id = p.id_client
                                       WHERE c.name=%s AND c.surname=%s AND c.email=%s AND p.number=%s
                                       """, (first_name, last_name, email, phone))
                        else:
                            cur.execute("""
                                       SELECT * FROM clients
                                       WHERE name=%s AND surname=%s AND email=%s
                                       """, (first_name, last_name, email))
                    else:
                        if phone:
                            cur.execute("""
                                       SELECT * FROM clients c 
                                       JOIN phones p on c.id = p.id_client
                                       WHERE c.name=%s AND c.surname=%s AND p.number=%s
                                       """, (first_name, last_name, phone))
                        else:
                            cur.execute("""
                                       SELECT * FROM clients
                                       WHERE name=%s AND surname=%s
                                       """, (first_name, last_name))
                else:
                    if email:
                        if phone:
                            cur.execute("""
                                       SELECT * FROM clients c 
                                       JOIN phones p on c.id = p.id_client
                                       WHERE c.email=%s AND p.number=%s
                                       """, (email, phone))
                        else:
                            cur.execute("""
                                       SELECT * FROM clients
                                       WHERE email=%s
                                       """, (email, ))
                    else:
                        if phone:
                            cur.execute("""
                                       SELECT * FROM phones 
                                       WHERE number=%s
                                       """, (phone, ))
            conn.commit()
            return cur.fetchall()