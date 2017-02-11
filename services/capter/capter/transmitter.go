package main

import (
	"log"
)

func transmit_patterns(places []Choice, sum int, pattern []byte) []int {
	var places_stored []int
	for place := range randSlice(places, sum) {
		err := store_pattern(place, pattern)
		if err == nil {
			places_stored = append(places_stored, place)
		}
		if len(places_stored) > 3 {
			break
		}
	}
	return places_stored
}

func store_pattern(place int, pattern []byte) error {
	log.Printf("%s stored to %s", pattern, place)
	return nil
}
