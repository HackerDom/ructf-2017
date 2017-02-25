package main

import (
	"strconv"
	"strings"
	"time"
)

func create_pattern(id, message string) ([]byte, string, string) {
	ts := strconv.FormatInt(time.Now().Unix(), 16) + "-"
	return []byte(id + ":" + message), "password", ts
}

func decode_pattern(pattern, password string) string {
	return strings.Split(pattern, ":")[1]
}
