from pathlib import Path
import sqlite3

from app import config


class SQLite:
    def __init__(self):
        self.path = Path(f'{config["DEFAULT"]["DB_PATH"]}/store.db')

    def __enter__(self):
        self.connection = sqlite3.connect(self.path)
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
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        description TEXT NOT NULL,
                        code TEXT NOT NULL,
                        cost INTEGER NOT NULL
                    )
                ''')
            except sqlite3.Error as error:
                print('Models:', error)

    def insert_model(self, description: str, code: str,  cost: int) -> None:
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
                cursor.execute('INSERT INTO coupon (description, code, cost) VALUES (?, ?, ?)',
                               (description, code, cost))
            except sqlite3.Error as error:
                print('Models:', error)

    def delete_model(self, coupon_id: int) -> None:
        '''
        Delete coupon.\n
        Params:
            coupon_id: int
            Coupon id to delete.
        '''
        with SQLite() as cursor:
            try:
                cursor.execute('DELETE FROM coupon WHERE id = ?',
                               (coupon_id, ))
            except sqlite3.Error as error:
                print('Models:', error)

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
                    'SELECT * FROM coupon WHERE id = ?', (coupon_id, ))
                return cursor.fetchone()[2:4]
            except sqlite3.Error as error:
                return error
            except TypeError as error:
                print('Models:', error)

    def show_coupons(self) -> list:
        '''
        Show the avaible coupons.
        '''
        with SQLite() as cursor:
            try:
                cursor.execute('SELECT id, description, cost FROM coupon')
            except sqlite3.Error as error:
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
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT NOT NULL,
                        value INTEGER NOT NULL,
                        coupon_id INTEGER,
                        FOREIGN KEY (coupon_id) REFERENCES coupon(id)
                    );
                ''')
            except sqlite3.Error as error:
                print('Models:', error)

    def insert_model(self, user_id: str, value: int, coupon_id: int = None) -> None:
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
                    VALUES (?, ?, ?);
                ''', (user_id, value, coupon_id, ))
            except sqlite3.Error as error:
                print('Models:', error)

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
                    SELECT user_id,
                    SUM(CASE
                        WHEN coupon_id THEN value * (-1)
                        ELSE value
                    END) AS Balance
                    FROM tx
                    WHERE user_id = ?
                ''', (user_id, ))
            except sqlite3.Error as error:
                print('Models:', error)
            else:
                return cursor.fetchone()[1] or 0
