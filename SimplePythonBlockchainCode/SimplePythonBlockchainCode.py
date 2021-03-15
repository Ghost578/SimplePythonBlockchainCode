

import datetime
import hashlib
import json
from flask import Flask, jsonify

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.create_genesis_block(proof = 1, previous_hash = '0')
        
    def create_genesis_block (self, proof, previous_hash):
        myBlock = {'index': len(self.chain) + 1,
                   'timemined': str(datetime.datetime.now()),
                   'proof': proof,
                   'previous_hash': previous_hash}
        self.chain.append(myBlock)
        return myBlock
    
    def get_previous_block(self):
        return self.chain[-1]
    
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    
    
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
            return new_proof
        
        
blockchain = shaanBlockchain()
app = Flask(__name__)

@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof =  previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_genesis_block(proof, previous_hash)
    response = {'index': block['index'],
                'timemined': block['timemined'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200
@app.route('/get_chain', methods=['GET'])


def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

app.run(host = '0.0.0.0', port = 5000)
        
