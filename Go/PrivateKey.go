// Implementação de Bilar (2014)
package main

import (
	"crypto/rand"
	"fmt"
	"math/big"
	"time"
)

// GERADOR DE NÚMEROS PSEUDOALEATÓRIO (Necessário para Delta, DeltaPrime e Ul)
type PseudoRandomNumberGenerator struct {
	seed        int64
	elementSize int
	listSize    int
	list        []*big.Int
}

// Construtor em forma de função (já que não tem classes em Go)
func NewGenerator(seed int64, elementSize, listSize int) *PseudoRandomNumberGenerator {
	return &PseudoRandomNumberGenerator{
		seed:        seed,
		elementSize: elementSize,
		listSize:    listSize,
		list:        make([]*big.Int, listSize),
	}
}

// Retorna um novo valor.
func (generator PseudoRandomNumberGenerator) NewValue() {
	for i := 0; i < generator.listSize; i++ {
		if generator.list[i] == nil {
			randomNumber, err := rand.Int(rand.Reader, big.NewInt(1<<uint(generator.elementSize)))

			if err != nil {
				panic(err)
			}

			generator.list[i] = randomNumber
		}
	}
}

func (generator PseudoRandomNumberGenerator) GetValue(index int) *big.Int {
	return generator.list[index]
}

// ESTRUTURA DE CHAVE PRIVADA (Esquema DGHV)
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

	startTimer := time.Now()

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

	timePassed := time.Since(startTimer)

	fmt.Printf("Tempo de Execução: %s\n", timePassed)
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
