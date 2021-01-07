# -*- coding: utf-8 -*-
"""
Key derivation from K_r and node ID =1 

@author: Gajraj Kuldeep
"""

import hashlib
from Cryptodome.Random import get_random_bytes
import numpy as np

K_r = get_random_bytes(16) # Master random vector key
K_p = get_random_bytes(16) # Master permutation key

salt = get_random_bytes(32)

node_id=b'01'

saltID=salt+node_id
K_r_1 = hashlib.pbkdf2_hmac('sha256', K_r, saltID, 100000,dklen=16)

#update salt value
salt = get_random_bytes(32)

node_id=b'01'

saltID=salt+node_id

K_p_1 = hashlib.pbkdf2_hmac('sha256', K_r, saltID, 100000,dklen=16)

np.save('keys/K_p_1',K_p_1)
np.save('keys/K_r_1',K_r_1)