class Transaction:
    def __init__(self,sender:str,recipient:str,amount:float) -> None:
        '''
            交易初始化
        '''
        self.sender=sender
        self.recipient=recipient
        self.amount=amount
        
    def __repr__(self) -> str:
        return f'Transactoion(from:{self.sender}, to:{self.recipient}, amount:{self.amount})'