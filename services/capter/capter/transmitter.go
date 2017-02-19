package main

import (
	"errors"
	"log"
	"net/http"
	"net/url"
	"time"
)

func transmit_patterns(places []Choice, sum int, id string, pattern []byte) []string {
	var places_stored []string
	for place := range randSlice(places, sum) {
		err := store_pattern(place, id, pattern)
		if err == nil {
			places_stored = append(places_stored, place)
		}
		if len(places_stored) > 3 {
			break
		}
	}
	return places_stored
}

func store_pattern(place, id string, pattern []byte) error {
	client := &http.Client{Timeout: time.Second * 10}
	response, err := client.PostForm(
		"http://"+place+":8081/",
		url.Values{"id": {id}, "pattern": {string(pattern)}})
	if err != nil {
		log.Print(err.Error())
		return err
	}
	if response.StatusCode != 201 {
		log.Printf("%s not stored to %s: %s", id, place, response.Status)
		return errors.New("Conflict")
	}
	log.Printf("%s stored to %s", id, place)
	return nil
}
