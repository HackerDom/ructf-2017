package main

import (
	"github.com/boltdb/bolt"
	"log"
	"strconv"
	"time"
)

type Capter struct {
	db       *bolt.DB
	patterns []byte
	places   []byte
}

func NewCapter() *Capter {
	capter := new(Capter)
	capter.patterns = []byte("patterns")
	capter.places = []byte("places")
	db, err := bolt.Open("db", 0600, &bolt.Options{Timeout: 1 * time.Second})
	if err != nil {
		log.Fatal(err)
	}
	db.Update(func(tx *bolt.Tx) error {
		_, err := tx.CreateBucket(capter.patterns)
		return err
	})

	// if db.places exists - skip
	db.Update(func(tx *bolt.Tx) error {
		_, err := tx.CreateBucket(capter.places)
		return err
	})
	for i := 1; i < 31; i++ {
		db.Update(func(tx *bolt.Tx) error {
			b := tx.Bucket(capter.places)
			err := b.Put([]byte(strconv.Itoa(i)), []byte(strconv.Itoa(1)))
			return err
		})
	}
	capter.db = db
	return capter
}

func (self *Capter) choose() ([]Choice, int) {
	var candidates []Choice
	sum := 0
	self.db.View(func(tx *bolt.Tx) error {
		p := tx.Bucket(self.places)
		p.ForEach(func(k, v []byte) error {
			sla, _ := strconv.Atoi(string(v))
			candidates = append(candidates, Choice{string(k), sla})
			sum += sla
			return nil
		})
		return nil
	})
	return candidates, sum
}

func (self *Capter) store(id, message string) error {
	pattern, password := create_pattern(id, message)
	candidates, sum := self.choose()
	places := transmit_patterns(candidates, sum, id, pattern)
	log.Print(places)
	self.db.Update(func(tx *bolt.Tx) error {
		b := tx.Bucket(self.patterns)
		// Change local message
		err := b.Put([]byte(id), password) // + places
		p := tx.Bucket(self.places)
		for _, place := range places {
			db_place := []byte(place)
			tries, _ := strconv.Atoi(string(p.Get(db_place)))
			err = p.Put(db_place, []byte(strconv.Itoa(tries+1)))
		}
		return err
	})
	return nil
}

func (self *Capter) get(id string) string {
	var answer string
	self.db.View(func(tx *bolt.Tx) error {
		answer = string(tx.Bucket(self.patterns).Get([]byte(id)))
		return nil
	})
	return answer
}
