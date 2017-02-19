package main

import (
	"math/rand"
)

func strInSlice(k string, list []string) bool {
	for _, b := range list {
		if b == k {
			return true
		}
	}
	return false
}

type Choice struct {
	Key    string
	Weight int
}

func randSlice(list []Choice, max_num int) chan string {
	slice := make(chan string)
	var choice []string

	go func() {
		for {
			r := rand.Intn(max_num)
			for _, c := range list {
				r -= c.Weight
				if r < 0 && !strInSlice(c.Key, choice) {
					slice <- c.Key
					choice = append(choice, c.Key)
					break
				}
			}
		}
		close(slice)
	}()
	return slice
}
