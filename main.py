#!/usr/bin/env python3

import os
import glob
import sys
import func as fx
import logger as lg
from blockchain_parser.blockchain import Blockchain
import json

# inits
blocks = []
json_indent = 4

def usage():
    print('Usage: {} [blocks_directory] [index_path] [storage_path]'.format(sys.argv[0]))
    sys.exit(1)


def save_data(blk_json):
    global storage_path
    file_path = os.path.join(storage_path, '{}.json'.format(blk_json['hash']))
    with open(file_path, 'w') as f:
        json.dump(blk_json, f, indent=json_indent)
    lg.success('[+] Block saved: {}'.format(blk_json['hash']))
    print('')


def process_block(block):
    global index_path
    #print(index_path)
    bc = Blockchain(block)
    for blk in bc.get_ordered_blocks(index_path):
        blk_json = {}
        # callable on a blk -> 'blk_file', 'from_hex', 'hash', 'header', 'height', 'hex', 'n_transactions', 'size', 'transactions'
        #print(blk.hash, blk.blk_file, blk.header.previous_block_hash, blk.height, blk.hex, blk.n_transactions, blk.size)
        blk_json.update({ 'hash': blk.hash, 'height': blk.height, 'size': blk.size, 'nTx': blk.n_transactions })
        lg.default('[-] Processing Block: {}'.format(blk.hash))
        for tx in blk.transactions:
            blk_tx = []
            lg.warning('[-] Found Tx: {}'.format(tx.hash))
            # callable on a tx -> 'from_hex', 'hash', 'hex', 'inputs', 'is_coinbase', 'is_segwit', 'locktime', 'n_inputs', 'n_outputs', 'outputs', 'size', 'txid', 'uses_bip69', 'uses_replace_by_fee', 'version', 'vsize'
            #print(tx.hash, tx.hex, tx.inputs, tx.is_coinbase(), tx.is_segwit, tx.locktime, tx.n_inputs, tx.n_outputs, tx.size, tx.txid, tx.uses_bip69(), tx.uses_replace_by_fee(), tx.version, tx.vsize)
            _tx = { 'txid': tx.txid, 'hash': tx.hash, 'version': tx.version, 'size': tx.size, 'vsize': tx.vsize, 'locktime': tx.locktime }
            _tx_inputs = []
            _tx_outputs = []
            for i in tx.inputs:
                v_in = {}
                # callables on input -> 'add_witness', 'from_hex', 'hex', 'script', 'sequence_number', 'size', 'transaction_hash', 'transaction_index', 'witnesses'
                #print(i.sequence_number, i.transaction_hash, i.transaction_index, i.witnesses, i.get_hex())
                v_in.update({ 'sequence': i.sequence_number, 'coinbase': i.transaction_hash })
                _tx_inputs.append(v_in)
            #print(tx.n_outputs, tx.outputs)
            for o in tx.outputs:
                v_out = {}
                # callables on output -> 'addresses', 'from_hex', 'is_multisig', 'is_p2sh', 'is_p2wpkh', 'is_p2wsh', 'is_pubkey', 'is_pubkeyhash', 'is_return', 'is_unknown', 'script', 'size', 'type', 'value'
                #print(o.addresses, o.is_multisig(), o.is_p2sh(), o.is_p2wpkh(), o.is_p2wsh(), o.is_pubkey(), o.is_pubkeyhash(), o.is_return(), o.is_unknown(), o.script, o.size, o.type, o.value)
                #print(dir(o.script))
                v_out.update({ 'value': o.value, 'scriptPubKey': { 'asm': o.script.value, 'type': o.type } })
                _tx_outputs.append(v_out)
            _tx.update({ 'vin': _tx_inputs, 'vout': _tx_outputs })
            blk_tx.append(_tx)
            blk_json.update({ 'tx': blk_tx })
            break
        #print(blk_json)
        save_data(blk_json)

if len(sys.argv) != 4:
    usage()


# all set
blocks_directory = sys.argv[1]
index_path = sys.argv[2]
storage_path = sys.argv[3]

if not fx.path_exists(storage_path):
    os.mkdir(storage_path)

# traverse through blocks directory
for file_name in glob.iglob(blocks_directory + '/**', recursive=True):
        if os.path.isfile(file_name) and fx.is_file_ext(file_name, 'dat'):
            process_block(file_name)
