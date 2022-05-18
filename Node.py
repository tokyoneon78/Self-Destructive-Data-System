import pickle
import logging
import asyncio

from kademlia.network import Server

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger('kademlia')
log.addHandler(handler)
log.setLevel(logging.DEBUG)

bootstrap_node = ("127.0.0.1", int("8468"))
loop = asyncio.get_event_loop()
loop.set_debug(True)

server = Server()
loop.run_until_complete(server.listen(8469))
loop.run_until_complete(server.bootstrap([bootstrap_node]))
loop.run_until_complete(server.set('name', pickle.dumps(["pls work for me", 5, 9])))

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    server.stop()
    loop.close()
