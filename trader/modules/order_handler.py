class BinanceHandler:
    def __init__(self):
        # Fake vlaues. TODO: Get it from DB
        self.api_key = 'poexi-139-04-3i0roijcldkmcçxl'
        self.api_secret = 'ijdoru20948ciekp3xijdo2q9wxk'
        # Outros instanciamentos...
    
    def execute_for_real(self, given_order):
        pass

    def check_for_real(self, order_to_check):
        pass

    def execute_in_backing_test(self, given_order):
        print('Hi, i am the backing test execute order. The order is:')
        print(' ')
        return given_order
        

    def check_in_backing_test(self, order_to_check):
        print('Hi, i am the check in backing test order')

    def execute(self, given_order, in_mode):
        if (in_mode == 'backing_test'): self.execute_in_backing_test(given_order)
        elif(in_mode == 'real_trade'): self.execute_for_real(given_order)
        else: print("Invalid mode. Must be 'backin_test' or 'real_trade'.")


    def check(self, order_to_check, in_mode):
        if (in_mode == 'backing_test'): self.check_in_backing_test(order_to_check)
        elif(in_mode == 'real_trade'): self.check_for_real(order_to_check)
        else: print("Invalid mode. Must be 'backin_test' or 'real_trade'.")