from solcx import compile_standard
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file =  file.read()

# Compile the solidity code

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol":{"content": simple_storage_file}},
        "settings": {
            "outputSelection":{
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },

    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# Get the Bytecode
bytecode = compiled_sol ["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

# Get the ABI
abi = compiled_sol ["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# For connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337
my_address = "0xA1B0C81b7D200bFb3dD77C30229032cCB2032E88"
private_key = os.getenv("PRIVATE_KEY")

# Create a contract
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the latest transaction
nonce = w3.eth.get_transaction_count(my_address)

# 1 Build a Transaction
# 2 Sign a Transaction
# 3 Send a Transaction

transaction = SimpleStorage.constructor().build_transaction(
    {"chainId":1337, "from":my_address, "nonce": nonce}
)

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# Send signed Transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)