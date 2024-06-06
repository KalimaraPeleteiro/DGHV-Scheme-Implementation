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

        self.f1 = PseudoRandomNumberGenerator(self.seed, parameters["gamma"], [parameters["tau"]])

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
        
        
        # ===== Passo 03 - Valor S =====
        