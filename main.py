
"""P = pow(2, 256) - pow(2, 32) - 977
A = 0
B = 7
Gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141"""

from ecc.ecc import *
from ecc.util import *
from tx.tx import *
from tx.script import *
from validate.op import *
from os import getcwd

def get_keys():
    if input("Avez-vous une clé ?") == "Oui":
        secret = int(input("Saisissez votre clé privée : "))
    else:
        secret = input("Saisissez une phrase secrète : ")
    return PrivateKey(secret)

def update_keyfile(key, filename):
    if not find_duplicate(key.secret, filename):
        with open(filename, "a") as backup:
            backup.write(str(key.secret) + '\n' + str(key.point) + '\n')
            print("backup saved in {}".format(filename))
    else:
        print("key already in file {}".format(filename))

def construct_tx(testnet=True):
    nb_inputs = int(input("nombre d'inputs : "))
    tx_ins = []
    for _ in range(nb_inputs):
        prev_tx, prev_index = input("id et index de l'UTXO à dépenser : ").split()
        prev_tx = bytes.fromhex(prev_tx)
        prev_index = int(prev_index)
        tx_ins.append(TxIn(prev_tx, prev_index))
    tx_outs = []
    nb_outputs = int(input("nombre d'outputs : "))
    for _ in range(nb_outputs):
        amount = int(float(input("Montant en BTC : ")) * 100000000)
        address = input("Adresse de destination : ")
        h160 = decode_base58(address)
        script_pubkey = p2pkh_script(h160) 
        tx_outs.append(TxOut(amount, script_pubkey))
        testnet = testnet
    return Tx(1, tx_ins, tx_outs, 0, testnet)

def sign_tx(tx):
    for index, tx_in in enumerate(tx.tx_ins):
        print("Signing input {}".format(tx_in))
        if tx_in.script_pubkey(testnet=tx.testnet).is_p2sh():
            keys = []
            while 1:
                key = PrivateKey.parse(input("Saisissez votre clé privée (WIF) : "))
                keys.append(key)
                if input("Continuer la saisie de clés ? Oui ou Non ") == "Non":
                    break
            redeem_script = input("Redeem Script ? ")
            tx.sign_input(index, keys, redeem_script)
        else:
            key = PrivateKey.parse(input("Saisissez votre clé privée (WIF) : "))
            tx.sign_input(index, key)
    return tx

def main():
    keys = get_keys()
    dirname = getcwd()
    filename = dirname + "/my_secret"
    update_keyfile(keys, filename)
    testnet = True

    while 1:
        action = input("""
            0 toggle testnet
            1 générer une adresse
            2 nouvelle transaction
            3 script
            4 voir la clé
            5 générer une nouvelle clé
            """)
        """if action == "0":
            if testnet == True:
                testnet = False
            else:
                testnet = True"""
        if action == "1":
            adress = keys.point.address(testnet=testnet)
            print(adress)
        elif action == "2":
            tx = construct_tx(testnet)
            print(tx)
            print(tx.serialize().hex())
            signed_tx = sign_tx(tx)
            print(signed_tx)
            print(signed_tx.serialize().hex())
            #tx.broadcast() 
        elif action == "3":
            #scriptgirl()
            continue
        elif action == "4":
            print("Clé privée : {}\nclé publique : {}".format(keys.secret, keys.point))
            print("Clé privée (WIF) : {}\n".format(keys.wif(testnet=testnet)))
            print("Clé publique (compressée) : {}\n".format(keys.point.sec().hex()))
            print("Clé publique (non compressée) : {}\n".format(keys.point.sec(compressed=False).hex()))
        elif action == "5":
            main()
        else:
            print("Choisissez une valeur entre 1 et 4")
            continue

if __name__ == "__main__":
    main()
