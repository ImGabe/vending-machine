from app.data.models import CouponModel, TxModel


class VendingMachine:
    def __init__(self):
        self.coupon = CouponModel()
        self.coupon.create_table()
        self.tx = TxModel()
        self.tx.create_table()

    def user_balance(self, user_id: str) -> int:
        '''
        Returns the user's credit.\n
        Params:
            user_id: str
            User ID to check credits.
        '''
        return self.tx.view_balance(user_id)

    def view_showcase(self) -> list:
        '''
        Return the available coupons.
        '''
        return self.coupon.show_coupons()

    def buy_coupon(self, user_id: str, coupon_id: int) -> (tuple, str):
        '''
        Purchase an available coupon.\n
        Params:
            user_id: str
            User ID to purchase a cupom.
            coupon_id: in
            Purchased Coupon ID.
        '''
        try:
            balance = self.tx.view_balance(user_id)
            coupon = self.coupon.get_coupon(coupon_id)
            [code, cost] = coupon

            if (balance - cost) >= 0:
                coupon_status = self.tx.insert_model(user_id, cost, coupon_id)
                return (*coupon_status, code)
            else:
                return ('err', 'Don\'t have enough money.')
        except (ValueError, TypeError):
            return ('err', 'This coupon doesn\'t exist.')
