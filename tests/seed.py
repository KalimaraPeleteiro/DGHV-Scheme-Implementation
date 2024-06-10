"""
time.time() pode não ser viável em um cenário de multi-thread. 

Talvez buscar outras possibilidades seja necessário.
"""

import time
import uuid
import os
import hashlib

# Opção 01 - time.time()
print(f"Opção Time - {int(time.time())}")

# Opção 02 - uuid usa os.unrandom por debaixo dos panos.
value = uuid.uuid4()
print(f"Opção UUID - {int(value.int)}")

# Opção 03 - hash com os.urandom
random_data = os.urandom(16)
hash_value = hashlib.sha256(random_data).digest()

print(f"Opção Hash - {int.from_bytes(hash_value, byteorder='big')}")
