"""
Autor: Roberto Peleteiro Galhardi
<kalimarapeleteiro@gmail.com>

Replicando Implementação de Bilar(2014)
"""

import random
from gmpy2 import mpz

class PseudoRandomNumberGenerator:

    # Parâmetros

    # seed -> Utilizado para a aleatoriedade
    # element_size -> Quantidade de Bits que o número aleatório gerado terá.
    # list_size -> Usado para definir o tamanho da lista gerada

    def __init__(self, seed, element_size, list_size) -> None:
        self.seed, self.gam, self.n = seed, element_size, list_size

        # Fazer range sobre um inteiro gera uma sequência do tamanho do valor dele
        self.list = [None for i in range(self.list_size)]
    
    def __getitem__(self, index): return self.list[index]
    
    def __setitem__(self, index, value): self.list[index] = value

    def __iter__(self):
        random.seed(self.seed)  # Setando a seed

        for i in range(self.list_size):

            # mpz é o formato utilizado para operações em gymp2. O resultado é convertido para esse formato.
            # getrandbits(x) gera um número aleatório inteiro de x bits.
            rand = mpz(random.getrandbits(self.element_size))

            if self.list[i] != None: 
                yield self.list[i]
            else:
                yield rand