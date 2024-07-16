# 首先创建一个区块链类（抽象基类）
class Blockchain(object):
    def __init__(self):
        self.chain=[]
        self.current_transactions=[]

    def new_block(self):
        '''创建一个新的区块，并放到链上'''
        pass

    def new_transaction(self):
        '''创建一个新的交易，并吧她加入到链上'''
        pass
    
    @staticmethod
    def hash(block):
        '''对区块做一次哈希'''
        pass

    @property
    def last_block(self):
        '''返回最后一个区块'''
        pass
