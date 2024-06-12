# Testando a Geração da Lista de Ruído DeltaPrime

from Parameters import *
from gmpy2 import mpz
from PseudoRandomNumberGenerator import PseudoRandomNumberGenerator

import random
import time
import uuid

counter1 = time.time()
value = uuid.uuid4()
f1 = PseudoRandomNumberGenerator(seed = int(value.int), element_size=LARGE["gam"], list_size=LARGE["Theta"])
counter1end = time.time()

print(f"F1: {f1}")
print("")
print(f"Tempo de Geração de f1: {counter1end - counter1:.2f} segundos.")

counter2 = time.time()

deltaPrime = [chi % PRIME_NUMBER_LARGE + 
                           random.randint(0, mpz(2) ** (LARGE["gam"] + 
                                                        LARGE["eta"]/PRIME_NUMBER_LARGE)/PRIME_NUMBER_LARGE) 
                                                        * PRIME_NUMBER_LARGE - 2 * random.randint(-mpz(2) ** LARGE["rho"], mpz(2) ** LARGE["rho"]) - si for chi, si in zip(f1, S_LARGE)]


counter2end = time.time()

print("")
print(f"Tempo de Geração de DeltaPrime: {counter2end - counter2:.2f} segundos.")