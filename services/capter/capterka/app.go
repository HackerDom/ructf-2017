package main

import (
	"net/http"
	"os"
)

func main() {
	kapterka := *NewKapterka()
	http.HandleFunc("/", kapterka.Index)
	port := "8081"
	if len(os.Args) > 1 {
		port = os.Args[1]
	}
	http.ListenAndServe(":"+port, nil)
}
