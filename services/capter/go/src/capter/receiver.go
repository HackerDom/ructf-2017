package main

import (
	"bytes"
	"errors"
	"io/ioutil"
	"log"
	"net/http"
	"time"
)

func receive_message(places []string, id, ts string) ([]string, string) {
	messages := make(map[string]int)
	var good_places []string
	for _, place := range places {
		if message, err := receive_one_message(place, id, ts); err == nil {
			good_places = append(good_places, place)
			messages[message] += 1
		}
	}
	var message string
	freq := 0
	for p, f := range messages {
		if f > freq {
			freq = f
			message = p
		}
	}
	return good_places, message
}

func receive_one_message(place, id, ts string) (string, error) {
	client := &http.Client{Timeout: time.Second * 1}
	response, err := client.Get(
		"http://" + place + ":8081/?id=" + ts + "-" + id)
	if err != nil {
		log.Print(err.Error())
		return "", err
	}
	if response.StatusCode != 200 {
		log.Printf("%s-%s not found on %s: %s", ts, id, place, response.Status)
		return "", errors.New("Not found")
	}
	defer response.Body.Close()
	answer, err := ioutil.ReadAll(response.Body)
	return string(bytes.TrimSpace(answer)), err
}
