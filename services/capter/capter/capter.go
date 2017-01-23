package main

import (
	"github.com/boltdb/bolt"
	"log"
	"time"
)

type Capter struct {
	db    *bolt.DB
	flags []byte
}

func NewCapter() *Capter {
	capter := new(Capter)
	capter.flags = []byte("flags")
	db, err := bolt.Open("local.db", 0600, &bolt.Options{Timeout: 1 * time.Second})
	if err != nil {
		log.Fatal(err)
	}
	db.Update(func(tx *bolt.Tx) error {
		_, err := tx.CreateBucket(capter.flags)
		return err
	})
	capter.db = db
	return capter
}

func (self *Capter) store(id, message string) error {
	self.db.Update(func(tx *bolt.Tx) error {
		b := tx.Bucket(self.flags)
		err := b.Put([]byte(id), []byte(message))
		return err
	})
	return nil
}

func (self *Capter) get(id string) string {
	var answer string
	self.db.View(func(tx *bolt.Tx) error {
		answer = string(tx.Bucket(self.flags).Get([]byte(id)))
		return nil
	})
	return answer
}
