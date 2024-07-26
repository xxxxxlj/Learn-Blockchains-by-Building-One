import hashlib
import random
from typing import List

# 定义交易类
class Transaction:
    def __init__(self, sender: str, recipient: str, amount: float):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def __repr__(self):
        return f"Transaction(from: {self.sender}, to: {self.recipient}, amount: {self.amount})"

# 定义区块类
class Block:
    def __init__(self, previous_hash: str, transactions: List[Transaction], timestamp: str):
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp
        self.block_hash = self.calculate_hash()

    def calculate_hash(self):
        transaction_str = ''.join([str(tx) for tx in self.transactions])
        block_data = f"{self.previous_hash}{transaction_str}{self.timestamp}"
        return hashlib.sha256(block_data.encode()).hexdigest()

    def __repr__(self):
        return f"Block(previous_hash: {self.previous_hash}, transactions: {self.transactions}, timestamp: {self.timestamp}, hash: {self.block_hash})"

# 定义账户类
class Account:
    def __init__(self, address: str, balance: float):
        self.address = address
        self.balance = balance

    def __repr__(self):
        return f"Account(address: {self.address}, balance: {self.balance})"

# 定义验证者类
class Validator:
    def __init__(self, address: str, stake: float):
        self.address = address
        self.stake = stake

    def __repr__(self):
        return f"Validator(address: {self.address}, stake: {self.stake})"

# 定义区块链类
class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.accounts = {}  # 存储账户和余额
        self.validators = []  # 存储验证者

    def create_genesis_block(self):
        # 创建创世区块
        genesis_block = Block("0", [], "2024-01-01T00:00:00")
        self.chain.append(genesis_block)

    def add_transaction(self, transaction: Transaction):
        self.current_transactions.append(transaction)

    def add_block(self, block: Block):
        # 验证区块并添加到链中
        if self.validate_block(block):
            self.chain.append(block)
            self.current_transactions = []  # 清空交易列表
        else:
            raise ValueError("Invalid block")

    def validate_block(self, block: Block) -> bool:
        # 验证区块的基本结构
        if not isinstance(block, Block):
            return False

        # 验证区块哈希
        return block.block_hash == block.calculate_hash()

    def validate_transaction(self, transaction: Transaction) -> bool:
        # 验证交易
        sender_balance = self.accounts.get(transaction.sender, 0)
        return sender_balance >= transaction.amount

    def validate_all_transactions(self):
        # 验证所有当前交易
        return all(self.validate_transaction(tx) for tx in self.current_transactions)

    def select_validator(self):
        # 简单的随机选择验证者
        total_stake = sum(v.stake for v in self.validators)
        choice = random.uniform(0, total_stake)
        cumulative_stake = 0
        for validator in self.validators:
            cumulative_stake += validator.stake
            if choice <= cumulative_stake:
                return validator
        return None

# 示例用法
blockchain = Blockchain()
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
    new_block = Block(blockchain.chain[-1].block_hash, blockchain.current_transactions, "2024-07-24T00:00:00")

    if blockchain.validate_all_transactions():
        blockchain.add_block(new_block)
        print(f"New block added by validator {selected_validator.address}: {new_block}")
    else:
        print("Invalid transactions in the block.")
else:
    print("No validator selected.")
