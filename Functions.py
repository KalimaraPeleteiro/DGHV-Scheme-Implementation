"""
Autor: Roberto Peleteiro Galhardi
<kalimarapeleteiro@gmail.com>

Replicando Implementação de Bilar(2014)
"""

from PseudoRandomNumberGenerator import PseudoRandomNumberGenerator
from gmpy2 import mpz
from utils.math import modNear

import random

def encrypt(publickKey, message):
    assert message == 0 or message == 1

    x0 = publickKey["pkAsk"]["x0"]
    f1 = PseudoRandomNumberGenerator(seed = publickKey["pkAsk"]["seed1"],
                                     element_size = publickKey["parameters"]["gamma"],
                                     list_size = publickKey["parameters"]["tau"])
    soma = 0

    for chi, delta in zip(f1, publickKey["pkAsk"]["delta"]):
        soma += (chi - delta) * random.randint(0, mpz(2) ** publickKey["parameters"]["alpha"])
    
    r = random.randint(-mpz(2)**publickKey["parameters"]["rho"], mpz(2)**publickKey["parameters"]["rho"])
    c = message + 2 * r + 2 * soma      # Faltando o ModNear para precisão
    return c