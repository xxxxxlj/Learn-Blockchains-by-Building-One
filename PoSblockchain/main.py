# from BlockChainAPI import BlockChainAPI

# if __name__=="__main__":
#     # parser=ArgumentParser()
#     # parser.add_argument('-p', '--port', default=6000, type=int, help='port to listen on')
#     # args = parser.parse_args()
#     # port = args.port

#     blockchain_api=BlockChainAPI()
#     blockchain_api.run(host='0.0.0.0',port=6001)

from Chain import Chain
from Validator import Validator
from Transacation import Transaction
from Block import Block


# 示例用法
blockchain = Chain()
blockchain.create_genesis_block()

# 创建账户
blockchain.accounts["Alice"] = 100
blockchain.accounts["Bob"] = 50

# 创建验证者
blockchain.validators.append(Validator("Alice", 30))
blockchain.validators.append(Validator("Bob", 20))

# 创建交易
tx1 = Transaction("Alice", "Bob", 10)
blockchain.add_transaction(tx1)

# 创建新区块
selected_validator = blockchain.select_validator()
if selected_validator:
    new_block = Block("2024-07-24T00:00:00",blockchain.current_transactions, blockchain.chain[-1].block_hash)
    if blockchain.validate_all_transactions():
        blockchain.add_block(new_block)
        print(f"New block added by validator {selected_validator.address}: {new_block}")
    else:
        print("Invalid transactions in the block.")
else:
    print("No validator selected.")
