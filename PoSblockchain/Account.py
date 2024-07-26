# 账户类
class Account:
    def __init__(self,address:str,balance:float) -> None:
        '''
            存放个人账户
        '''
        self.address:address
        self.balance:balance

    def __repr__(self):
        return f"Account(address: {self.address}, balance: {self.balance})"