"""
Autor: Roberto Peleteiro Galhardi
<kalimarapeleteiro@gmail.com>

Replicando Implementação de Bilar(2014)
"""

from gmpy2 import mpz

import gmpy2
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