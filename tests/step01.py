# Testando Escolha de Número Primo e Vetor S

from Parameters import *
from gmpy2 import next_prime

import random
import time


# Função para Vetor S
def random_list(size):
    myList = [0 for i in range(size)]
    myList[random.randint(0, size - 1)] = 1

    return myList




# Análise
counter1 = time.time()
while True:
    prime_number = next_prime(random.getrandbits(TOY["eta"]))

    if len(prime_number) == TOY["eta"]:
        counter1end = time.time()
        break

print(f"Número primo escolhido: {prime_number}")
print("")
print(f"Tempo de Escolha do Número Primo: {counter1end - counter1:.2f} segundos.")
print(f"Tamanho do Número: {len(prime_number)}")


counter2 = time.time()

assert TOY["Theta"] % 15 == 0
size = int(TOY["Theta"]/15)
s = [1] + [0 for i in range(size - 1)]

for i in range(15 - 1):
    s = s + random_list(size)

counter2end = time.time()


print("")
print("")
print(f"Vetor S Gerado: {s}")
print("")
print(f"Tempo de Criação do Vetor: {counter2end - counter2:.2f} segundos.")
print(f"Tamanho do Vetor: {len(s)}")
