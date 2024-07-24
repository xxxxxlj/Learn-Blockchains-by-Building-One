class Transaction:
    def __init__(self,sender,recipient,amount) -> None:
        '''
            交易初始化
        '''
        self.sender=sender
        self.recipient=recipient
        self.amount=amount
        
   
    @property
    def to_dict(self):
        return {
            "sender":self.sender,
            "recipient":self.recipient,
            "amount":self.amount,
        }