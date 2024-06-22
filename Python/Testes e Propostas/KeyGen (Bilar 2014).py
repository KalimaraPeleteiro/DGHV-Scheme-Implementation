# Calculando Velocidade de KeyGen com Bilar (2014)

from Parameters import *
from gmpy2 import mpz, next_prime
from PseudoRandomNumberGenerator import PseudoRandomNumberGenerator

import time
import random
import uuid
import pickle


# Função para Vetor S
def random_list(size):
    myList = [0 for i in range(size)]
    myList[random.randint(0, size - 1)] = 1

    return myList


def main():
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


    # Passo 02 - q0 e x0
    q0 = random.randint(0, mpz(2) ** TOY["gam"]/prime_number)
    x0 = q0 * prime_number


    # Passo 03 - Lista Delta
    value1 = uuid.uuid4()
    f1 = PseudoRandomNumberGenerator(seed = int(value1.int), element_size=TOY["gam"], list_size=TOY["tau"])

    delta = [(chi % prime_number) + prime_number -
                        random.randint(0, mpz(2) ** (TOY["lam"]) + 
                                        TOY["eta"] * prime_number - 
                                        random.randint(- (mpz(2) ** TOY["rho"]), 
                                                        mpz(2)**TOY["rho"])) for chi in f1]


    # Passo 04 - Elemento ul
    kappa = TOY["gam"] + TOY["eta"] + 2
    value2 = uuid.uuid4()
    f2 = PseudoRandomNumberGenerator(seed = int(value2.int), 
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
    value3 = uuid.uuid4()
    f3 = PseudoRandomNumberGenerator(seed = int(value3.int), element_size=TOY["gam"], list_size=TOY["Theta"])

    deltaPrime = [chi % prime_number + 
                            random.randint(0, mpz(2) ** (TOY["gam"] + 
                                                            TOY["eta"]/prime_number)/prime_number) 
                                                            * prime_number - 2 * random.randint(-mpz(2) ** TOY["rho"], mpz(2) ** TOY["rho"]) - si for chi, si in zip(f3, s)]


    counter1end = time.time()

    pkAsk = {"seed01": value1, "x0": x0, "delta": delta}
    PublicKey = {"pkAsk": pkAsk, "seed2": value2, "ul": ul,
                          "seed3": value3, "deltaPrime": deltaPrime, 
                          "parameters": TOY}
    
    with open("PublicKey - Toy (Bilar 2014).bin", "wb") as f:
        pickle.dump(PublicKey, f)


    # print(f"Tempo Final de Execução: {counter1end - counter1:.2f} segundos")

if __name__ == "__main__":
    main()
