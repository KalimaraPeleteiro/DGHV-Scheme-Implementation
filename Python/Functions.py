"""
Autor: Roberto Peleteiro Galhardi
<kalimarapeleteiro@gmail.com>

Replicando Implementação de Bilar(2014)
"""

from PseudoRandomNumberGenerator import PseudoRandomNumberGenerator
from gmpy2 import mpz

import gmpy2
import random

def quocientNear(a, b):
    return (2 * a + b) // (2 * b)

def modNear(a, b):
    return a - b * quocientNear(a, b)


def encrypt(publickKey, message):
    assert message == 0 or message == 1

    x0 = publickKey["pkAsk"]["x0"]
    f1 = PseudoRandomNumberGenerator(seed = publickKey["pkAsk"]["seed1"],
                                     element_size = publickKey["parameters"]["gamma"],
                                     list_size = publickKey["parameters"]["tau"])
    soma = 0

    for chi, delta in zip(f1, publickKey["pkAsk"]["delta"]):
        soma += (chi - delta) * random.randint(0, mpz(2) ** publickKey["parameters"]["alpha"])
    
    randomness = random.randint(-mpz(2)**publickKey["parameters"]["rho"], mpz(2)**publickKey["parameters"]["rho"])
    cipher = message + 2 * randomness + 2 * soma      # Faltando o ModNear para precisão
    return cipher


def expand(publicKey, cipher):
    n = 4 
    parameters = publicKey["parameters"]

    kappa = parameters["gamma"] + parameters["eta"] + 2
    f2 = PseudoRandomNumberGenerator(seed = publicKey["seed2"],
                                     element_size = kappa + 1, 
                                     list_size = parameters["Theta"])
    
    f2[0] = publicKey["ul"]
    gmpy2.get_context().precision = 30000

    k = mpz(2) ** kappa
    y = [u/k for u in f2]
    z = [cipher * yi for yi in y]

    gmpy2.get_context().precision = n

    zprime = [float(zi) for zi in z]
    gmpy2.get_context().precision = 30000

    return zprime


def decrypt(secretKey, cipher, z):
    e = zip(secretKey, z)
    soma = 0
    for si, zi in zip(secretKey, z):
        soma += si * zi
    
    soma = int(round(soma))
    message = (cipher - soma) % 2

    return message