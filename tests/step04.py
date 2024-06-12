# Testando criação do elemento Ul

from Parameters import *
from PseudoRandomNumberGenerator import PseudoRandomNumberGenerator
from gmpy2 import mpz

import uuid 
import time

counter1 = time.time()
kappa = TOY["gam"] + TOY["eta"] + 2
value = uuid.uuid4()
f1 = PseudoRandomNumberGenerator(seed = int(value.int), 
                                 element_size=kappa, list_size=TOY["Theta"])
f1[0] = 0
counter1end = time.time()

print(f"F1: {f1}")
print("")
print(f"Tempo de Geração de f1: {counter1end - counter1:.2f} segundos.")

counter2 = time.time()
somatorio = 0
i = 0
for u in f1:
    somatorio += u * S_TOY[i]  # Multiplica o número aleatório gerado pelo índice em Vetor S
    i += 1
soma = mpz(round((mpz(2) ** kappa)/PRIME_NUMBER_TOY))
ul = soma-somatorio
counter2end = time.time()

print(f"UL: {ul}")
print("")
print(f"Tempo de Geração de ul: {counter2end - counter2:.2f} segundos.")
