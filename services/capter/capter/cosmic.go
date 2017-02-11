package main

import (
	"math/rand"
)

func intInSlice(i int, list []int) bool {
	for _, b := range list {
		if b == i {
			return true
		}
	}
	return false
}

type Choice struct {
	Num    int
	Weight int
}

func randSlice(list []Choice, max_num int) chan int {
	slice := make(chan int)
	var choice []int

	go func() {
		for {
			r := rand.Intn(max_num)
			for _, c := range list {
				r -= c.Weight
				if r < 0 && !intInSlice(c.Num, choice) {
					slice <- c.Num
					choice = append(choice, c.Num)
					break
				}
			}
		}
		close(slice)
	}()
	return slice
}
