from pathlib import Path

import psycopg2

from app import config


class SQLite:
    def __init__(self):
        pass

    def __enter__(self):
        self.connection = psycopg2.connect(f'dbname={config["DB"]["DB_NAME"]} user={config["DB"]["USER"]}')
        return self.connection.cursor()

    def __exit__(self, *args):
        try:
            self.connection.commit()
        except:
            self.connection.rollback()
        finally:
            self.connection.close()


class CouponModel:
    def create_table(self) -> None:
        '''
        Create a table if it doesn't exist.
        '''
        with SQLite() as cursor:
            try:
                cursor.execute('''
                    CREATE TABLE IF NOT exists coupon (
                        id SERIAL PRIMARY KEY,
                        description TEXT NOT NULL,
                        code TEXT NOT NULL,
                        cost INTEGER NOT NULL
                    )
                ''')
            except Exception as error:
                print('Models:', error)

    def insert_model(self, description: str, code: str,  cost: int) -> str:
        '''
        Insert a model.\n
        Params:
            description: str
            Description of cupon.
            code: str
            Code of cupon.
            cost: int
            Cost of cupon.
        '''
        with SQLite() as cursor:
            try:
                cursor.execute('INSERT INTO coupon (description, code, cost) VALUES (%s, %s, %s)',
                               (description, code, cost))
            except Exception as error:
                return error
            else:
                return 'Ok!'

    def get_coupon(self, coupon_id: int) -> tuple:
        '''
        Get coupon information.\n
        Params:
            coupon_id: int
            Coupon id to get
        '''
        with SQLite() as cursor:
            try:
                cursor.execute(
                    'SELECT * FROM coupon WHERE id = %s', (coupon_id, ))
                return cursor.fetchone()[2:4]
            except Exception as error:
                print('Models:', error)

    def show_coupons(self) -> list:
        '''
        Show the avaible coupons.
        '''
        with SQLite() as cursor:
            try:
                cursor.execute('''
                    SELECT c.id, description, cost FROM coupon AS c
                    LEFT JOIN tx AS t ON t.coupon_id = c.id
                    WHERE t.coupon_id IS NULL
                ''')
            except Exception as error:
                print('Models:', error)
            else:
                return cursor.fetchall()


class TxModel():
    def create_table(self) -> None:
        '''
        Create a table if it doesn't exist.
        '''
        with SQLite() as cursor:
            try:
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS tx (
                        id SERIAL PRIMARY KEY,
                        user_id TEXT NOT NULL,
                        value INTEGER NOT NULL,
                        coupon_id INTEGER UNIQUE,
                        FOREIGN KEY (coupon_id) REFERENCES coupon(id)
                    );
                ''')
            except Exception as error:
                print('Models:', error)

    def insert_model(self, user_id: str, value: int, coupon_id: int = None) -> (str, str):
        '''
        Insert a model.\n
        Params:
            user_id: str
            User ID to receive credits or purchase a coupon.
            value: int
            Value to receive or of the coupon.
            coupon_id: int
            Purchased Coupon ID.
        '''
        with SQLite() as cursor:
            try:
                cursor.execute('''
                    INSERT INTO tx (user_id, value, coupon_id)
                    VALUES (%s, %s, %s);
                ''', (user_id, value, coupon_id, ))
            except psycopg2.IntegrityError as error:
                return ('err', 'It has already been purchased.')
            except Exception as error:
                return ('err', error)
            else:
                return ('ok', 'Approved.')

    def view_balance(self, user_id: str) -> int:
        '''
        Searches the database for user credit.\n
        Params:
            user_id: str
            User ID to check credits
        '''
        with SQLite() as cursor:
            try:
                cursor.execute('''
                    SELECT SUM(
                        CASE 
                            WHEN coupon_id IS NOT NULL THEN value * (-1) 
                            ELSE value 
                        END) AS Balance 
                        FROM tx 
                        WHERE user_id = '%s'
                ''', (user_id, ))
            except Exception as error:
                print('Models:', error)
            else:
                return cursor.fetchone()[0] or 0
