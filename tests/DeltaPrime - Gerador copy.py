# Tentando Aplicar Geradores em DeltaPrime e Delta

from Parameters import *
from gmpy2 import mpz, next_prime
from PseudoRandomNumberGenerator import PseudoRandomNumberGenerator
from joblib import Parallel, delayed

import time
import random
import uuid


# Função para Vetor S
def random_list(size):
    myList = [0 for i in range(size)]
    myList[random.randint(0, size - 1)] = 1

    return myList


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


def computeDeltaPrimeValues(prime_number, chi, si):
    value1 = chi % prime_number
    value2 = random.randint(0, 2 ** (MEDIUM["gam"] + MEDIUM["eta"]/prime_number)/prime_number)
    value3 = prime_number - 2 * random.randint(2 ** MEDIUM["rho"], 2 ** MEDIUM["rho"]) - si

    result = value1 + value2 * value3
    return result


def deltaPrimeWithGenerator(prime_number, s):
    counter = time.time()
    value = uuid.uuid4()
    f3 = PseudoRandomNumberGenerator(seed = int(value.int), element_size=MEDIUM["gam"], list_size=MEDIUM["Theta"])
  
    deltaPrime = Parallel(n_jobs=-1)(delayed(computeDeltaPrimeValues)(prime_number, chi, si) for chi, si in zip(f3, s))

    counterend = time.time()

    print(f"Tempo de Execução Paralelo: {counterend - counter:.2f} segundos")






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

