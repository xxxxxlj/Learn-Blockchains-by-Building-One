from Block import Block
from Transacation import Transaction
from time import time
import random

# 区块链类
class Chain:
    def __init__(self) -> None:
        '''
            初始化链
        '''
        self.chain=[]
        self.current_transactions=[]
        self.accounts={}
        self.validators=[]

    def create_genesis_block(self)->None:
        '''
            构造创世区块
        '''
        genesis_block=Block(str(time()),self.current_transactions,'0')
        self.chain.append(genesis_block)

    def add_transaction(self,transaction:Transaction)->None:
        '''
            增加交易
        '''
        if not isinstance(transaction,Transaction):
            raise TypeError
        self.current_transactions.append(transaction)

    def add_block(self,block:Block)->None:
        '''
            增加区块
        '''
        if self.validate_block(block):
            self.chain.append(block)
            self.current_transactions=[]    # 清空交易数组
        else:
            raise ValueError('Invalid block')
        
    def validate_block(self,block:Block)->bool:
        '''
            验证区块是否正确
        '''
        if not isinstance(block, Block):
            return False
        return block.block_hash == block.hash()
    
    def validate_transaction(self,transaction:Transaction)->bool:
        '''
            验证交易，确保交易发出者的账户内能够支付交易金额，否则交易无法进行
        '''
        sender_balance=self.accounts.get(transaction.sender,0)
        return sender_balance>=transaction.amount
       
    
    def validate_all_transactions(self)->bool:
        '''
            验证所有的交易
        '''
        return all(self.validate_transaction(tr) for tr in self.current_transactions)
    
    def select_validator(self):
        '''
            累加法选择验证者
        '''
        total_stake=sum(tx.stake for tx in self.validators)
        choice=random.uniform(0,total_stake)
        cumulative_stake=0
        for validator in self.validators:
            cumulative_stake+=validator.stake
            if cumulative_stake>=choice:
                return validator
        return None