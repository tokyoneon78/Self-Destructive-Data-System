from cryptography.fernet import Fernet
import sys
import ssss
from kademlia.network import Server
import asyncio
import random
import pickle

def write_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    """
    Loads the key from the current directory named `key.key`
    """
    return open("key.key", "rb").read()

def encrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it encrypts the file and write it
    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read all file data
        file_data = file.read()
    # encrypt data
    encrypted_data = f.encrypt(file_data)
    # write the encrypted file
    with open(filename, "wb") as file:
        file.write(encrypted_data)

def decrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it decrypts the file and write it
    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()
    # decrypt data
    decrypted_data = f.decrypt(encrypted_data)
    # write the original file
    with open(filename, "wb") as file:
        file.write(decrypted_data)

def load_encrypted_file(filename):
    opened_file = open(filename, "r")
    return opened_file.read()

def split_password_file(file, pieces, recon_piece):
    split_file = ssss.split(file, pieces, recon_piece)
    #print(split_file)
    return split_file

def generate_seed():
    return random.randint(0, 100000)



def node_selections(pieces):
    l = []
    count = pieces
    while (count > 0):
        random.seed(count)
        l.append(random.randint(1, 1000))
        count -= 1
    l.append(random.randint(1, 1000))
    return l


if len(sys.argv) != 4:
    print("Usage: python Main.py <File name> <Shares> <Threshold>")
    sys.exit(1)

write_key()
key = load_key()

#encrypt(sys.argv[1], key)

split_pass = split_password_file(key, int(sys.argv[2]), int(sys.argv[3]))
payload = load_encrypted_file(sys.argv[1])



seed = generate_seed()

nodes = node_selections(int(sys.argv[2]))

final_node = pickle.dumps([payload, int(sys.argv[2]), int(sys.argv[3])])

bootstrap_node = ("127.0.0.1", int("8468"))
loop = asyncio.get_event_loop()
loop.set_debug(True)

server = Server()
loop.run_until_complete(server.listen(8495))
loop.run_until_complete(server.bootstrap([bootstrap_node]))
for i in range(len(split_pass)):
    print(split_pass[i][1])
    loop.run_until_complete(server.set(nodes[i], split_pass[i][1]))
loop.run_until_complete(server.set(str(nodes[i+1]), final_node))
print(nodes[i+1])

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    server.stop()
    loop.close()
