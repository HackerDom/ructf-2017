package main

import (
	"strings"
)

func create_pattern(id, message string) ([]byte, string) {
	return []byte(id + ":" + message), "password"
}

func decode_pattern(pattern, password string) string {
	return strings.Split(pattern, ":")[1]
}
