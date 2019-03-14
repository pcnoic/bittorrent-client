import random

#generating the peer-id randomly with below format:
#-<2 character id><4 digit version number>-<random numbers>

peer_id = '-PC0001-' + ''.join([str(random.randint(0, 9)) for _ in range(12)])
