import psycopg
def drop_table(user, host, dbname):
    """
    Function to create new database. 
    """
    conn = psycopg.connect(f"dbname={dbname} user={user} host={host}")
    cur = conn.cursor()
    query = f"""
            DROP TABLE IF EXISTS spending_data;
            """
    cur.execute(query)
    conn.commit()


def create_tables(user, host, dbname):
    """
    For the given user, host, and dbname,
    this function creates a table for the current month.
    The schema of each table is the following.
    MM_YYYY:
    date - TIMESTAMP, not null
    description - varying character (length of 100), not null
    type - varying character (length of 50), not null
    amount_spent - REAL, not null
    credit/debit - varying character (length of 10), not null
    """
    conn = psycopg.connect(f"dbname={dbname} user={user} host={host}")
    cur = conn.cursor()
    spending_data =\
                """
                CREATE TABLE spending_data
                (   
                    id SERIAL PRIMARY KEY,
                    date TIMESTAMP NOT NULL,
                    description VARCHAR(100) NOT NULL,
                    type VARCHAR(50) NOT NULL,
                    amount_spent REAL NOT NULL,
                    credit_debit VARCHAR(10) NOT NULL
                );
                """
    cur.execute(spending_data)
    conn.commit()


def copy_data(user, host, dbname, dir):
    """
    Using user, host, dbname, and dir,
    this function connects to the database and
    loads data to spending_data table from the csv file
    from data.csv which is located in dir.
    Note: each file includes a header.
    """
    with psycopg.connect(f"user='{user}' \
                         host='{host}' \
                         dbname='{dbname}'") as conn:
        with conn.cursor() as curs:
            spending_data =\
                f"""
                COPY spending_data(Date, Description, Type, Amount_Spent,Credit_Debit)
                FROM '{dir}/data.csv'
                DELIMITER ','
                CSV HEADER;
                """
            curs.execute(spending_data)

        conn.commit()

def read_fulltable(user, host, dbname): 
    """
    Function to read the table
    """
    conn = psycopg.connect(f"dbname={dbname} user={user} host={host}")
    cur = conn.cursor()
    query = f"""
            SELECT * FROM spending_data;
            """
    cur.execute(query)
    conn.commit()
    return cur.fetchall()

drop_table('postgres', 'localhost', 'spending_db')
create_tables('postgres', 'localhost', 'spending_db')
copy_data('postgres', 'localhost', 'spending_db', '/Users/rashmipanse/Documents/Projects/PersonalFinanceDash')


