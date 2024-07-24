from flask import Flask,jsonify,request
from uuid import uuid4

from Chain import Chain

class BlockChainAPI:
    def __init__(self) -> None:
        '''
            初始化Flask后端
        '''
        self.app=Flask(__name__)
        self.nodeidentifier=str(uuid4()).replace('-','')
        self.blockchain=Chain()
        self.setup_routes()     

    def setup_routes(self):
        '''
            所有的路由都一次性注册完毕
        '''
        self.app.add_url_rule('/mine', 'mine', self.mine, methods=['GET'])
        self.app.add_url_rule('/transactions/new', 'new_transaction', self.new_transaction, methods=['POST'])
        self.app.add_url_rule('/chain', 'full_chain', self.full_chain, methods=['GET'])
        self.app.add_url_rule('/nodes/register', 'register_node', self.register_node, methods=['POST'])
        self.app.add_url_rule('/nodes/resolve', 'consensus', self.consensus, methods=['GET'])

    def mine(self):
        '''
            挖掘后端
        '''
        last_block=self.blockchain.last_block
        proof=self.blockchain.proof_of_work(last_block)
    
        # 构建新交易，
        # sender设置为’0‘表明这是新挖出来的区块
        self.blockchain.new_transaction(
            sender='0',
            recipient=self.nodeidentifier,
            amount=1
        )
        previous_hash=self.blockchain.hash(last_block)
        block=self.blockchain.new_block(proof,previous_hash)

        response={
            'message':"New block forged",
            'index':block["index"],
            'transactions':block["transactions"],
            'proof':block['proof'],
            'previous_hash':block["previous_hash"]
        }
        return jsonify(response),200

    def new_transaction(self):
        '''
            创建新交易后端
        '''
        values=request.get_json()

        # 检查创建新交易的元素是否都在上传的API中
        required=["sender","recipient","amount"]
        if not all(k in values for k in required):
            return 'Missing values',400
        
        # 创建新的交易
        index=self.blockchain.new_transaction(values["sender"],values["recipient"],values["amount"])
        response={'message':f'Transaction will be added to Block {index}'}
        return jsonify(response),201

    def full_chain(self):
        '''
            查看全链后端
        '''
        response={
            'chain':self.blockchain.chain,
            'length':len(self.blockchain.chain)
        }
        return jsonify(response),200
    
    def register_node(self):
        '''
            注册结点
        '''
        values=request.get_json()

        nodes=values.get('nodes')
        if nodes is None:
            return "Error: Please supply a valid list of nodes", 400
        
        for node in nodes:
            self.blockchain.register_node(node)

        response={
            "message":'New nodes have been added',
            "total_nodes":list(self.blockchain.nodes)
        }
        return jsonify(response),201
    
    def consensus(self):
        '''
            共识后端
        '''
        repalced=self.blockchain.resolve_conflicts()
        if repalced:
            response = {
                'message': 'Our chain was replaced',
                'new_chain': self.blockchain.chain
            }
        else:
            response = {
                'message': 'Our chain is authoritative',
                'chain': self.blockchain.chain
            }

        return jsonify(response), 200
    
    def run(self, host='0.0.0.0', port=6000):
        '''
            后端运行函数
        '''
        self.app.run(host=host, port=port)