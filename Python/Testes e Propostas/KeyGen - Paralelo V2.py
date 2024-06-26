# Calculando Velocidade de KeyGen com Bilar (2014) + Parelelo + deltaPrime Paralelo

from Parameters import *
from gmpy2 import mpz, next_prime
from PseudoRandomNumberGenerator import PseudoRandomNumberGenerator
from joblib import Parallel, delayed

import time
import random
import uuid
import multiprocessing 



# Função para Vetor S
def random_list(size):
    myList = [0 for i in range(size)]
    myList[random.randint(0, size - 1)] = 1

    return myList


# Passo 02 - q0 e x0
def step_02(prime_number):
    q0 = random.randint(0, mpz(2) ** SMALL["gam"]/prime_number)
    x0 = q0 * prime_number


# Passo 03 - Lista Delta
def step_03(prime_number):
    value = uuid.uuid4()
    f1 = PseudoRandomNumberGenerator(seed = int(value.int), element_size=SMALL["gam"], list_size=SMALL["tau"])

    delta = [(chi % prime_number) + prime_number -
                        random.randint(0, mpz(2) ** (SMALL["lam"]) + 
                                        SMALL["eta"] * prime_number - 
                                           random.randint(- (mpz(2) ** SMALL["rho"]), 
                                                        mpz(2)**SMALL["rho"])) for chi in f1]


# Passo 04 - Elemento ul
def step_04(prime_number, s):
    kappa = SMALL["gam"] + SMALL["eta"] + 2
    value = uuid.uuid4()
    f2 = PseudoRandomNumberGenerator(seed = int(value.int), 
                                    element_size=kappa, list_size=SMALL["Theta"])
    f2[0] = 0

    somatorio = 0
    i = 0
    for u in f2:
        somatorio += u * s[i]  # Multiplica o número aleatório gerado pelo índice em Vetor S
        i += 1
    soma = mpz(round((mpz(2) ** kappa)/prime_number))
    ul = soma-somatorio


def computeDeltaPrimeValues(prime_number, chi, si):
    value1 = chi % prime_number
    value2 = random.randint(0, 2 ** (SMALL["gam"] + SMALL["eta"]/prime_number)/prime_number)
    value3 = prime_number - 2 * random.randint(-2 ** SMALL["rho"], 2 ** SMALL["rho"]) - si

    result = value1 + value2 * value3
    return result


# Passo 05 - Lista DeltaPrime
def step_05(prime_number, s):
    value = uuid.uuid4()
    f3 = PseudoRandomNumberGenerator(seed = int(value.int), element_size=SMALL["gam"], list_size=SMALL["Theta"])
    deltaPrime = Parallel(n_jobs=-1)(delayed(computeDeltaPrimeValues)(prime_number, chi, si) for chi, si in zip(f3, s))

    """
    deltaPrime = [chi % prime_number + 
                            random.randint(0, mpz(2) ** (SMALL["gam"] + 
                                                            SMALL["eta"]/prime_number)/prime_number) 
                                                            * prime_number - 2 * random.randint(-mpz(2) ** SMALL["rho"], mpz(2) ** SMALL["rho"]) - si for chi, si in zip(f3, s)]
    """





counter1end = time.time()

if __name__ == '__main__':

    # Passo 01 - Número Primo e Vetor S
    counter1 = time.time()

    # Escolhendo Número Primo
    while True:
        prime_number = next_prime(random.getrandbits(SMALL["eta"]))

        if len(prime_number) == SMALL["eta"]:
            break

    # Criando Vetor S
    assert SMALL["Theta"] % 15 == 0
    size = int(SMALL["Theta"]/15)
    s = [1] + [0 for i in range(size - 1)]

    for i in range(15 - 1):
        s = s + random_list(size)


    # Criando os 4 processos
    processes = [multiprocessing.Process(target=step_02, args=(prime_number,)), 
                 multiprocessing.Process(target=step_03, args=(prime_number,)),
                 multiprocessing.Process(target=step_04, args=(prime_number, s)),
                 multiprocessing.Process(target=step_05, args=(prime_number, s))]
    
    for p in processes:
        p.start()

    # Espera todos os processos terminarem
    for p in processes:
        p.join()
    
    counter1end = time.time()

    print(f"Tempo Final de Execução: {counter1end - counter1:.2f} segundos")
