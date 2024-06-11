# Testando a Definição de q0 e x0

from Parameters import *
from gmpy2 import mpz

import random
import time

counter1 = time.time()
q0 = random.randint(0, mpz(2) ** TOY["gam"]/PRIME_NUMBER_TOY)
counter1end = time.time()

print(f"q0: {q0}")
print("")
print(f"Tempo de Escolha de q0: {counter1end - counter1:.2f} segundos.")

counter2 = time.time()
x0 = q0 * PRIME_NUMBER_TOY
counter2end = time.time()
print("")
print("")
print(f"x0: {x0}")
print("")
print(f"Tempo de Escolha de x0: {counter2end - counter2:.2f} segundos.")