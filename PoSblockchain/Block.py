from typing import List
from Transacation import Transaction
import hashlib

class Block:
    '''
        区块类，完成区块的创建
    '''
    def __init__(self,timestamp:str,transactions:List[Transaction],previous_hash:str) -> None:
        '''
            初始化区块
        '''
        self.timestamp=timestamp
        self.transactions=transactions
        self.previous_hash=previous_hash
        self.block_hash=self.hash()

    def hash(self):
        '''
            计算区块哈希
        '''
        transaction_str = ''.join([str(tx) for tx in self.transactions])
        block_data = f"{self.previous_hash}{transaction_str}{self.timestamp}"
        return hashlib.sha256(block_data.encode()).hexdigest()
    
    def __repr__(self) -> str:
        return f'Block(previous_hash:{self.previous_hash},transactions:{self.transactions},timestamp:{self.timestamp},hash:{self.block_hash})'