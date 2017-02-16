package main

import (
	"github.com/syndtr/goleveldb/leveldb"
	"net/http"
	"os"
)

func main() {
	db, err := leveldb.OpenFile("capterka.db", nil)
	defer db.Close()
	http.HandleFunc("/get/", Get)
	http.HandleFunc("/put/", Put)
	port := "8081"
	if len(os.Args) > 1 {
		port = os.Args[1]
	}
	http.ListenAndServe(":"+port, nil)
}
