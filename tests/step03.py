# Testando a Geração da Lista de Ruído Delta

from Parameters import *
from gmpy2 import mpz
from PseudoRandomNumberGenerator import PseudoRandomNumberGenerator

import random
import time
import uuid

counter1 = time.time()
value = uuid.uuid4()
f1 = PseudoRandomNumberGenerator(seed = int(value.int), element_size=TOY["gam"], list_size=TOY["tau"])
counter1end = time.time()

print(f"F1: {f1}")
print("")
print(f"Tempo de Geração de f1: {counter1end - counter1:.2f} segundos.")

counter2 = time.time()

delta = [(chi % PRIME_NUMBER_TOY) + PRIME_NUMBER_TOY -
                       random.randint(0, mpz(2) ** (TOY["lam"]) + 
                                      TOY["eta"] * PRIME_NUMBER_TOY - 
                                      random.randint(- (mpz(2) ** TOY["rho"]), 
                                                     mpz(2)**TOY["rho"])) for chi in f1]

counter2end = time.time()

print(f"Delta: {delta}")
print("")
print(f"Tempo de Geração de Delta: {counter2end - counter2:.2f} segundos.")