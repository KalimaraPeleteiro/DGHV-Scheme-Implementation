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

	exponationValue := new(big.Int).Exp(big.NewInt(2), pk.gamma, nil)
	upperLimit := new(big.Int).Div(exponationValue, primeNumber)

	q0, err := rand.Int(rand.Reader, upperLimit)
	if err != nil {
		fmt.Println("Erro na geração de q0: ", err)
	}

	x0 := new(big.Int).Mul(q0, primeNumber)

	fmt.Println(x0)
}

func main() {

	// Parâmetro de Chave Toy
	key := PrivateKey{
		securityType:   "Toy",
		lambda:         42,
		rho:            26,
		eta:            988,
		gamma:          big.NewInt(147456),
		theta:          150,
		publickKeySize: 0.076519,
		securityLevel:  42,
		alpha:          936,
		tau:            158,
	}

	key.KeyGen()
}
