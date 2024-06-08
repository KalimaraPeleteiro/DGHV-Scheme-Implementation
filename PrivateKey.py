"""
Autor: Roberto Peleteiro Galhardi
<kalimarapeleteiro@gmail.com>

Replicando Implementação de Bilar(2014)
"""

from gmpy2 import mpz
from PseudoRandomNumberGenerator import PseudoRandomNumberGenerator

import gmpy2
import time
import random


# Função que cria uma lista de tamanho size, composta apenas por 0s, exceto um índice aleatório, de valor 1.
def random_list(size):
    myList = [0 for i in range(size)]
    myList[random.randint(0, size - 1)] = 1

    return myList


class PrivateKey:

    # O __init__ é o KeyGen
    def __init__(self, parameters) -> None:
        self.parameters = parameters

        
        # ===== Passo 01 - Gerar Número Primo, q0 e x0 =====
        # A função next_prime traz o próximo número primo em sequência. Caso passe 10, retorna 11.
        while True:
            self.prime_number = gmpy2.next_prime(random.getrandbits(parameters["eta"]))

            if len(self.prime_number) == parameters["eta"]:
                break
        
        # q0 é um valor entre 0 e 2^Gamma/Número Primo
        self.q0 = random.randint(0, (mpz(2) ** parameters["gamma"])/self.prime_number)

        # x0 é o produto de q0 e o número primo gerado.
        self.x0 = self.q0 * self.prime_number


        # ===== Passo 02 - Lista de Ruído Delta =====
        self.seed = int(time.time())    # Seed usando o horário do PC.

        self.f1 = PseudoRandomNumberGenerator(seed=self.seed, element_size=parameters["gamma"], 
                                              list_size=[parameters["tau"]])

        # --- Lista Delta ---
        # x = O resto da divisão de um número aleatório e o número primo escolhido.
        # y = A diferença do número primo com um valor entre 0 e 2^Lambda
        # z = A diferença do número primo com um valor entre -2**Rho e +2 **Rho

        # Com cada valor delta sendo d, temos:
        # d = x + y + eta * z
        self.delta = [(chi % self.prime_number) + self.prime_number -
                       random.randint(0, mpz(2) ** (parameters["lambda"]) + 
                                      parameters["eta"] * self.prime_number - 
                                      random.randint(- (mpz(2) ** parameters["rho"]), 
                                                     mpz(2)**parameters["rho"])) for chi in self.f1]
        
        
        # ===== Passo 03 - Vetor S =====
        
        # O tamanho da lista deve ser um múltiplo de 15
        assert parameters["theta"] % 15 == 0

        # Criação do Vetor no final irá gerar um Vetor S
        # Vetor S terá Theta Elementos, com Theta/15 elementos tendo valor 1 e todos os outros com valor 0.
        size = int(parameters["theta"]/15)
        self.s = [1] + [0 for i in range(size - 1)]
        for i in range(15 - 1):
            self.s = self.s + random_list(size)
        

        # ===== Passo 04 - Elemento Ul =====

        # Kappa = Gamma + Eta + 2
        self.kappa = parameters["gamma"] + parameters["eta"] + 2
        self.seed2 = int(time.time())

        # Segunda lista PseudoAleatória
        self.f2 = PseudoRandomNumberGenerator(seed=self.seed2, 
                                              element_size=self.kappa, 
                                              list_size=parameters["theta"])
        self.f2[0] = 0
        somatorio = 0
        i = 0
        for u in self.f2:
            somatorio += u * self.s[i]  # Multiplica o número aleatório gerado pelo índice em Vetor S
            i += 1
        soma = mpz(round((mpz(2) ** self.kappa)/self.prime_number))
        self.ul = soma-somatorio

        # ul é uma combinação de valores pseudoaleatórios gerados em f2, ponderados pelos valores do Vetor S
        # aleatoriamente, com o ajuste final de soma-somatório garantindo que ele esteja dentro de um 
        # certo limite.


        # ===== Passo 05 - DeltaPrime =====
        self.seed3 = int(time.time())
        self.f3 = PseudoRandomNumberGenerator(seed = self.seed2, element_size=parameters["gamma"],
                                              list_size=parameters["theta"])
        
        # Delta Prime é uma lista de valores aonde:

        # Para cada par de elemento X (Gerado Aleatoriamente) e si (Elemento Aleatório do Vetor S) temos:
        # x mod prime_number -> Para garantir que o resultado fique dentro do intervalo.
        # Um valor aleatório y é criado usando gamma e eta, para introduzir aleatoriedade.
        # Outro valor aleatório w é criado usando rho.
        
        # Gerando o resultado:
        # Cada elemento d de Delta Prime é, tendo:
        # y = número aleatório entre 0 e 2^((gamma + (eta/primo))/primo)
        # w = número aleatório entre -2^rho e 2^rho

        # d = x mod primo + y - w - si
        self.deltaPrime = [chi % self.prime_number + 
                           random.randint(0, mpz(2) ** (parameters["gamma"] + 
                                                        parameters["eta"]/self.prime_number)/self.prime_number) 
                                                        * self.prime_number - 2 * random.randint(-mpz(2) ** parameters["rho"], mpz(2) ** parameters["rho"]) - si for chi, si in zip(self.f3, self.s)]



        # ===== Passo 06 - Geração de Chave =====

        # self.PkAsk é "PublicKey Ask?" ou "solicitação de chave pública", informações necessárias
        # para solicitar ou recuperar a chave?

        # Chave Pública é composta por:
        # O Dicionário PkAsk, com seed1, o reticulado x0 e a lista delta de ruído.
        # Seed2 e Seed3
        # O elemento ul
        # A lista de ruído DeltaPrime
        # A lista de Parâmetros

        # A Chave Privada (Secret Key) é o Vetor S
        self.pkAsk = {"seed01": self.seed, "x0": self.x0, "delta": self.delta}
        self.PublicKey = {"pkAsk": self.pkAsk, "seed2": self.seed2, "ul": self.ul,
                          "seed3": self.seed3, "deltaPrime": self.deltaPrime, 
                          "parameters": self.parameters}
        
        self.SecretKey = self.s  # Chave Privada