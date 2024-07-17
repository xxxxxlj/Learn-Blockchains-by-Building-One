from time import time
import json
import hashlib

from flask import Flask,jsonify,request
from uuid import uuid4

import requests
from urllib.parse import urlparse

# 区块链类
class Blockchain(object):

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
        # 组装区块
        block={
            "index":len(self.chain)+1,
            "timestamp":time(),
            "transactions":self.current_transactions,
            "proof":proof,
            "previous_hash":previous_hash or self.hash(self.chain[-1])  
            # 前一个区块的哈希可能为空，所以需要计算一下
        }
        # 重置交易链
        self.current_transactions=[]
        # 区块上链
        self.chain.append(block)
        # 返回新区块
        return block
        

    def new_transaction(self,sender,recipient,amount):
        '''
            创建一个新的交易,
            sender <str> 发送者地址,
            recipient <str> 接受者地址,
            amount <int> 交易金额,
            返回值是本次交易的下标
        '''
        self.current_transactions.append({
            "sender":sender,
            "recipient":recipient,
            "amount":amount,
        })
        return self.last_block["index"]+1

        
    @staticmethod
    def hash(block):
        '''
            对区块做一次 Sha-256 哈希
            block <dict> block
            返回值 <str> 哈希值
        '''
        # 哈希必须保证字典是有序的，否则会出现哈希不一致的情况
        # 理论上Python3.7版本后不需要设置sort-keys=true，因为字典插入顺序自动有序，
        # 但是为兼容之前版本，保证准确运行仍然设置
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

            if response.status_code==200:
                length=response.json()['length']
                chain=response.json()['chain']

                # 判断区块链长度是不是比自己长，并且是合法的链
                if length>max_length and self.valid_chain(chain):
                    max_length=length
                    new_chain=chain

        if new_chain:
            self.chain=new_chain
            return True
        
        return False


# API调用
app=Flask(__name__)
nodeidentifier=str(uuid4()).replace('-','')

# 初始化区块链
blockchain=Blockchain()

@app.route('/mine',methods=['GET'])
def mine():
    '''
        工作量计算，获得下一个区块的证明
        返回状态情况
    '''
    last_block=blockchain.last_block
    proof=blockchain.proof_of_work(last_block)
    
    # 构建新交易，
    # sender设置为’0‘表明这是新挖出来的区块
    blockchain.new_transaction(
        sender='0',
        recipient=nodeidentifier,
        amount=1
    )
    previous_hash=blockchain.hash(last_block)
    block=blockchain.new_block(proof,previous_hash)

    response={
        'message':"New block forged",
        'index':block["index"],
        'transactions':block["transactions"],
        'proof':block['proof'],
        'previous_hash':block["previous_hash"]
    }
    return jsonify(response),200

@app.route('/transactions/new',methods=["POST"])
def new_transactions():
    '''
        创建新的交易
    '''
    values=request.get_json()

    # 检查创建新交易的元素是否都在上传的API中
    required=["sender","recipient","amount"]
    if not all(k in values for k in required):
        return 'Missing values',400
    
    # 创建新的交易
    index=blockchain.new_transaction(values["sender"],values["recipient"],values["amount"])
    response={'message':f'Transaction will be added to Block {index}'}
    return jsonify(response),201


@app.route('/chain',methods=['GET'])
def full_chain():
    '''
        查看整条链
    '''
    response={
        'chain':blockchain.chain,
        'length':len(blockchain.chain)
    }
    return jsonify(response),200

@app.route('/nodes/register',methods=['POST'])
def register_node():
    '''
        注册结点
    '''
    values=request.get_json()

    nodes=values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400
    
    for node in nodes:
        blockchain.register_node(node)

    response={
        "message":'New nodes have been added',
        "total_nodes":list(blockchain.nodes)
    }
    return jsonify(response),201

@app.route('/nodes/resolve',methods=['GET'])
def consensus():
    '''
        运行共识机制的请求
    '''
    repalced=blockchain.resolve_conflicts()
    if repalced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200

if __name__=='__main__':
    from argparse import ArgumentParser

    parser=ArgumentParser()
    parser.add_argument('-p', '--port', default=6000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
