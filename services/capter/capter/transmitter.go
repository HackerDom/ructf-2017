package main

import (
	"errors"
	"log"
	"net/http"
	"net/url"
	"time"
)

func transmit_patterns(places []Choice, sum int, id, ts string, pattern string) []string {
	var places_stored []string
	for place := range randSlice(places, sum) {
		err := store_pattern(place, id, ts, pattern)
		if err == nil {
			places_stored = append(places_stored, place)
		}
		if len(places_stored) > 3 {
			break
		}
	}
	return places_stored
}

func store_pattern(place, id, ts, pattern string) error {
	client := &http.Client{Timeout: time.Second * 1}
	response, err := client.PostForm(
		"http://"+place+":8081/",
		url.Values{"id": {ts + "-" + id}, "pattern": {pattern}})
	if err != nil {
		log.Print(err.Error())
		return err
	}
	if response.StatusCode != 201 {
		log.Printf("%s-%s not stored to %s: %s", ts, id, place, response.Status)
		return errors.New("Conflict")
	}
	return nil
}
