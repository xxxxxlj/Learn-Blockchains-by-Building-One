from Node import Node
class Block:
    def __init__(self,index,timestamp,transactions,proof,previous_hash,validator:Node) -> None:
        '''
            初始化区块
        '''
        self.index=index
        self.timestamp=timestamp
        self.transactions=transactions
        self.proof=proof
        self.previous_hash=previous_hash
        self.validator=validator

    @property
    def to_dict(self):
        '''
            将数据以字典形式返回
        '''
        return {
            "index":self.index,
            "timestamp":self.timestamp,
            "validator":self.validator,
            "transactions":[tx for tx in self.transactions],    # Transaction是一个数组，可见blockExample.json示例
            "proof":self.proof,
            "previous_hash":self.previous_hash 
        }