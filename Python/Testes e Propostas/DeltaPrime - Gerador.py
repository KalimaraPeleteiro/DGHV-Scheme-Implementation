# Tentando Aplicar Geradores em DeltaPrime e Delta

from Parameters import *
from gmpy2 import mpz, next_prime
from PseudoRandomNumberGenerator import PseudoRandomNumberGenerator

import time
import random
import uuid
from memory_profiler import profile


# Função para Vetor S
def random_list(size):
    myList = [0 for i in range(size)]
    myList[random.randint(0, size - 1)] = 1

    return myList


@profile
def deltaPrime(prime_number, s):
    counter = time.time()
    value = uuid.uuid4()
    f3 = PseudoRandomNumberGenerator(seed = int(value.int), element_size=MEDIUM["gam"], list_size=MEDIUM["Theta"])
    

    deltaPrime = [chi % prime_number + 
                            random.randint(0, mpz(2) ** (MEDIUM["gam"] + 
                                                            MEDIUM["eta"]/prime_number)/prime_number) 
                                                            * prime_number - 2 * random.randint(-mpz(2) ** MEDIUM["rho"], mpz(2) ** MEDIUM["rho"]) - si for chi, si in zip(f3, s)]
    counterend = time.time()

    print(f"Tempo de Execução sem Gerador: {counterend - counter:.2f} segundos")


@profile
def deltaPrimeWithGenerator(prime_number, s):
    counter = time.time()
    value = uuid.uuid4()
    f3 = PseudoRandomNumberGenerator(seed = int(value.int), element_size=MEDIUM["gam"], list_size=MEDIUM["Theta"])
  
    def deltaPrime_generator():
        for chi, si in zip(f3, s):
            if chi is None or si is None:
                break
            delta_prime = chi % prime_number + \
                          random.randint(0, mpz(2) ** (MEDIUM["gam"] + MEDIUM["eta"]/prime_number) / prime_number) * prime_number \
                          - 2 * random.randint(-mpz(2) ** MEDIUM["rho"], mpz(2) ** MEDIUM["rho"]) - si
            yield delta_prime
    
    
    delta_prime = list(deltaPrime_generator())

    counterend = time.time()

    print(f"Tempo de Execução com Gerador: {counterend - counter:.2f} segundos")





if __name__ == '__main__':

    # Escolhendo Número Primo
    while True:
        prime_number = next_prime(random.getrandbits(MEDIUM["eta"]))

        if len(prime_number) == MEDIUM["eta"]:
            break

    # Criando Vetor S
    assert MEDIUM["Theta"] % 15 == 0
    size = int(MEDIUM["Theta"]/15)
    s = [1] + [0 for i in range(size - 1)]

    for i in range(15 - 1):
        s = s + random_list(size)
    
    deltaPrime(prime_number, s)

    deltaPrimeWithGenerator(prime_number, s)

