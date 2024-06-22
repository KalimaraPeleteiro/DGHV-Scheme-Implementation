// Implementação de Bilar (2014)
package main

import (
	"crypto/rand"
	"fmt"
	"math/big"
)

type PrivateKey struct {
	securityType   string
	lambda         int
	rho            int
	eta            int
	gamma          *big.Int
	theta          int
	publickKeySize float64
	securityLevel  int
	alpha          int
	tau            int
}

func (pk PrivateKey) KeyGen() {

	var primeNumber *big.Int
	var err error

	// Passo 01 - Número Primo, q0 e x0
	for {
		primeNumber, err = rand.Prime(rand.Reader, pk.eta)

		if err != nil {
			fmt.Println("Erro na geração de número primo: ", err)
			continue
		}

		if primeNumber.BitLen() == pk.eta {
			break
		}
	}

	quotient := new(big.Int).Div(pk.gamma, primeNumber)

	upperLimit := new(big.Int).Exp(big.NewInt(2), quotient, nil)

	q0, err := rand.Int(rand.Reader, upperLimit)
	if err != nil {
		fmt.Println("Erro na geração de q0: ", err)
	}

	x0 := new(big.Int).Mul(q0, primeNumber)

	fmt.Println(x0)
}
