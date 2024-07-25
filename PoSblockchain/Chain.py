from time import time
import json
import hashlib
import requests
import random
from urllib.parse import urlparse

from Block import Block
from Transacation import Transaction
from Node import Node

class Chain(object):
    def __init__(self):
        '''
            初始化链
        '''
        self.chain=[]
        self.current_transactions=[]
        self.nodes=[Node("http://127.0.0.1:6000",5)] # 使用集合是希望集合中结点只出现一次
        # 首先要有一个创世区块
        self.new_block(previous_hash='1',proof=100)

    def register_node(self,address,stake):
        '''
            注册结点
            address 结点地址，如'192.0.0.2:5000' 
        '''
        node=Node(address,stake)
        node.register(self.nodes)

    def new_block(self,proof,previous_hash=None):
        '''
            在区块链中创建一个新的区块
            proof <int> 用于工作量机制
            previous_hash <str> 前一个区块的哈希值
            返回值 <dict> 新区块
        '''

        validator=self.proof_of_stake()
        block=Block(len(self.chain)+1,time(),self.current_transactions,
                    proof,previous_hash or self.hash(self.chain[-1]),validator)      
        self.current_transactions=[]
        self.chain.append(block.to_dict)        # 最后一定要to_dict
        validator.stake+=5                      # 验证者奖励
        return block.to_dict

    def new_transaction(self,sender,recipient,amount):
        '''
            创建一个新的交易,
            sender <str> 发送者地址,
            recipient <str> 接受者地址,
            amount <int> 交易金额,
            返回值是本次交易的下标
        '''
        transaction=Transaction(sender,recipient,amount).to_dict
        self.current_transactions.append(transaction)
        return self.last_block["index"]+1

        
    @staticmethod
    def hash(block):
        '''
            对区块做一次 Sha-256 哈希
            block <dict> block
            返回值 <str> 哈希值
        '''
        block_string=json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()     # sha256转换后转成str

    @property
    def last_block(self):
        '''
            返回最后一个区块
        '''
        return self.chain[-1]
    
    def proof_of_stake(self)->Node:
        '''
            权益证明：选出一个验证者
            返回 <Node> 验证者结点
        '''
        # 计算权益总和
        total_stake=sum(node.stake for node in self.nodes)
        # 随机选择权益
        select_point=random.uniform(0,total_stake)
        # 累加法得到选中的权益
        current_point=0
        for node in self.nodes:
            current_point+=node.stake
            if current_point>=select_point:
                return node
            
    def valid_chain(self,chain)->bool:
        '''
            判断两条区块链是否为相同
            chain <list> 区块链
            返回值 <bool> True为真，Fasle为否
        '''
        for i in range(min(len(self.chain),len(chain))):
            if self.hash(self.chain[i])!=self.hash(chain[i]):
                return False
        return True

  
    def resolve_conflicts(self)->bool:
        '''
            在验证区块链的过程中会发现错误，此时就需要根据共识解决冲突
            这里用网络中最长且通过验证的链来替代自己的链
            返回值 <bool> True表示解决冲突，False表示别没解决
        '''
        neighbours=self.nodes
        new_chain=None

        # 只考虑比自己长的链
        max_length=len(self.chain)

        # 验证网络中所有结点的区块链
        for node in neighbours:
            print(f'http://{node.netloc}/chain')
            response=requests.get(f'http://{node.netloc}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                print(chain[0]["validator"])
                chain = [
                    Block(
                        index=block["index"],
                        timestamp=block["timestamp"],
                        transactions=[Transaction(**tx).to_dict for tx in block["transactions"]],
                        proof=block["proof"],
                        previous_hash=block["previous_hash"],
                        validator=block["validator"]
                    ).to_dict
                    for block in chain
                ]
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain=new_chain
            return True
        
        return False