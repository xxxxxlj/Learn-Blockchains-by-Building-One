from time import time
import json
import hashlib
import requests
from urllib.parse import urlparse

from Block import Block
from Transacation import Transaction

class Chain(object):
    def __init__(self):
        self.chain=[]
        self.current_transactions=[]
        # 首先要有一个创世区块
        self.new_block(previous_hash='1',proof=100)
        # 区块链是去中心化的，因此区块链类需要一个节点集合
        self.nodes=set() # 使用集合是希望集合中结点只出现一次

    def register_node(self,address):
        '''
            注册结点
            address 结点地址，如'192.0.0.2:5000' 
        '''
        parsed_url=urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')

    def new_block(self,proof,previous_hash=None):
        '''
            在区块链中创建一个新的区块
            proof <int> 用于工作量机制
            previous_hash <str> 前一个区块的哈希值
            返回值 <dict> 新区块
        '''
        block=Block(len(self.chain)+1,time(),self.current_transactions,
                    proof,previous_hash or self.hash(self.chain[-1]))      # 最后一定要to_dict
        self.current_transactions=[]
        self.chain.append(block.to_dict)
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
    
    def proof_of_work(self,last_block)->int:
        '''
            工作量证明实现
            找到一个p'，使得hash(pp')的前四位为0
            p是前一个证明，p'是后一个证明
            last_block <dict> 上一个区块，从区块获取last_proof
            返回值 <int>
        '''
        last_proof=last_block["proof"]
        
        proof=0
        while self.valid_proof(last_proof,proof) is False:  # 调用内置的算法进行验证
            proof+=1
        return proof

    @staticmethod
    def valid_proof(last_proof,proof)->bool:
        '''
            判断是否hash值的前4位为0
            last_proof <int> 前一个证明
            proof <int> 当前证明
            返回值 <bool> True 为成功，False为失败
        '''
        # 先将两个证明拼接起来
        guess=f'{last_proof}{proof}'.encode()
        # 转成hash
        guess_hash=hashlib.sha256(guess).hexdigest()
        # 判断前四位是否为0
        return guess_hash[:4]=='0000'
    
    def valid_chain(self,chain)->bool:
        '''
            判断一条区块链是否为正确的，需要使用共识机制，该函数主要供节点使用
            chain <list> 区块链
            返回值 <bool> True为真，Fasle为否
        '''
        last_block=chain[0]
        current_index=1

        while current_index<len(chain):
            block= chain[current_index]

            # 先检查区块的上一个区块哈希是否正确
            last_block_hash=self.hash(last_block)
            if block['previous_hash']!=last_block_hash:
                return False
            # 然后检查区块的证明是否真确
            if not self.valid_proof(last_block['proof'],block['proof']):
                return False
            
            last_block=block
            current_index+=1
            
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
            response=requests.get(f'http://{node}/chain')


            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                chain = [
                    Block(
                        index=block["index"],
                        timestamp=block["timestamp"],
                        transactions=[Transaction(**tx).to_dict for tx in block["transactions"]],
                        proof=block["proof"],
                        previous_hash=block["previous_hash"]
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