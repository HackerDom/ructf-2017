package main

import (
	"github.com/syndtr/goleveldb/leveldb"
	"log"
	"net/http"
	"os"
)

type Capterca struct {
	db *leveldb.DB
}

func NewCapterca() *Capterca {
	capterca := new(Capterca)
	db, err := leveldb.OpenFile("db", nil)
	if err != nil {
		log.Fatal(err)
	}
	capterca.db = db
	return capterca
}

func (self *Capterca) Get(w http.ResponseWriter, r *http.Request) {
	if err := r.ParseForm(); err != nil {
		http.Error(w, "Try again", http.StatusBadRequest)
		return
	}
	id := r.FormValue("id")
	if id == "" {
		http.Error(w, "Nice weather, isn't it?", http.StatusNoContent)
		return
	}
	if pattern, err := self.db.Get([]byte(id), nil); err == nil {
		http.Error(w, string(pattern), http.StatusOK)
	} else {
		http.Error(w, "", http.StatusNotFound)
	}
}

func (self *Capterca) Put(w http.ResponseWriter, r *http.Request) {
	if err := r.ParseForm(); err != nil {
		http.Error(w, "Try again", http.StatusBadRequest)
		return
	}
	id := r.FormValue("id")
	if id == "" {
		http.Error(w, "Do you really want it?", http.StatusBadRequest)
		return
	}
	if ret, _ := self.db.Has([]byte(id), nil); ret {
		http.Error(w, "", http.StatusConflict)
		return
	}
	pattern := r.FormValue("pattern")
	if pattern == "" {
		http.Error(w, "Where is the box?", http.StatusBadRequest)
		return
	}
	if err := self.db.Put([]byte(id), []byte(pattern), nil); err != nil {
		http.Error(w, "I'm a teapot", http.StatusInternalServerError)
		return
	} else {
		http.Error(w, "", http.StatusCreated)
	}
}

func (self *Capterca) Index(w http.ResponseWriter, r *http.Request) {
	switch method := r.Method; method {
	case "GET":
		self.Get(w, r)
	case "POST":
		self.Put(w, r)
	default:
		http.Error(w, "Try again", http.StatusMethodNotAllowed)
	}
}

func main() {
	capterca := *NewCapterca()
	http.HandleFunc("/", capterca.Index)
	port := "8081"
	if len(os.Args) > 1 {
		port = os.Args[1]
	}
	http.ListenAndServe(":"+port, nil)
}
