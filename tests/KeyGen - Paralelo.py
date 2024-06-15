# Calculando Velocidade de KeyGen com Bilar (2014) + Parelelo

from Parameters import *
from gmpy2 import mpz, next_prime
from PseudoRandomNumberGenerator import PseudoRandomNumberGenerator

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
    q0 = random.randint(0, mpz(2) ** TOY["gam"]/prime_number)
    x0 = q0 * prime_number


# Passo 03 - Lista Delta
def step_03(prime_number):
    value = uuid.uuid4()
    f1 = PseudoRandomNumberGenerator(seed = int(value.int), element_size=TOY["gam"], list_size=TOY["tau"])

    delta = [(chi % prime_number) + prime_number -
                        random.randint(0, mpz(2) ** (TOY["lam"]) + 
                                        TOY["eta"] * prime_number - 
                                        random.randint(- (mpz(2) ** TOY["rho"]), 
                                                        mpz(2)**TOY["rho"])) for chi in f1]


# Passo 04 - Elemento ul
def step_04(prime_number, s):
    kappa = TOY["gam"] + TOY["eta"] + 2
    value = uuid.uuid4()
    f2 = PseudoRandomNumberGenerator(seed = int(value.int), 
                                    element_size=kappa, list_size=TOY["Theta"])
    f2[0] = 0

    somatorio = 0
    i = 0
    for u in f2:
        somatorio += u * s[i]  # Multiplica o número aleatório gerado pelo índice em Vetor S
        i += 1
    soma = mpz(round((mpz(2) ** kappa)/prime_number))
    ul = soma-somatorio


# Passo 05 - Lista DeltaPrime
def step_05(prime_number, s):
    value = uuid.uuid4()
    f3 = PseudoRandomNumberGenerator(seed = int(value.int), element_size=TOY["gam"], list_size=TOY["Theta"])

    deltaPrime = [chi % prime_number + 
                            random.randint(0, mpz(2) ** (TOY["gam"] + 
                                                            TOY["eta"]/prime_number)/prime_number) 
                                                            * prime_number - 2 * random.randint(-mpz(2) ** TOY["rho"], mpz(2) ** TOY["rho"]) - si for chi, si in zip(f3, s)]






counter1end = time.time()

if __name__ == '__main__':

    # Passo 01 - Número Primo e Vetor S
    counter1 = time.time()

    # Escolhendo Número Primo
    while True:
        prime_number = next_prime(random.getrandbits(TOY["eta"]))

        if len(prime_number) == TOY["eta"]:
            break

    # Criando Vetor S
    assert TOY["Theta"] % 15 == 0
    size = int(TOY["Theta"]/15)
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
