package main

import (
	"bytes"
	"errors"
	"fmt"
	"github.com/boltdb/bolt"
	"log"
	"sort"
	"strconv"
	"strings"
	"time"
)

type Capter struct {
	db       *bolt.DB
	patterns []byte
	places   []byte
}

type TopArgs struct {
	Limit int
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
		_, err := tx.CreateBucketIfNotExists(capter.patterns)
		return err
	})

	db.Update(func(tx *bolt.Tx) error {
		b, err := tx.CreateBucket(capter.places)
		if err != nil {
			return err
		}
		for i := 1; i < 33; i++ {
			if err := b.Put([]byte("capter.team"+strconv.Itoa(i)+".ructf"), []byte(strconv.Itoa(1))); err != nil {
				return err
			}
		}
		return nil
	})
	capter.db = db
	return capter
}

func (self *Capter) get_places() ([]Choice, int) {
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
	sort.Slice(candidates, func(i, j int) bool { return candidates[i].Weight > candidates[j].Weight })
	return candidates, sum
}

func (self *Capter) Top(args *TopArgs, reply *string) error {
	places, _ := self.get_places()
	limit := args.Limit
	if limit > len(places) {
		limit = len(places)
	}
	var buffer bytes.Buffer
	for i := 0; i < limit; i++ {
		buffer.WriteString(fmt.Sprintf("%v:\t%v\n", places[i].Key, places[i].Weight))
	}
	*reply = buffer.String()
	if reply == nil {
		return errors.New("All hope is gone")
	}
	return nil
}

func (self *Capter) store(id, message string) error {
	var local_message string
	self.db.View(func(tx *bolt.Tx) error {
		local_message = string(tx.Bucket(self.patterns).Get([]byte(id)))
		return nil
	})
	if local_message != "" {
		return errors.New("409 Conflict")
	}
	pattern, password, ts := create_pattern(message)
	candidates, sum := self.get_places()
	places := transmit_messages(candidates, sum, id, ts, pattern)
	if len(places) < 2 {
		return errors.New("Not enough places")
	}
	self.db.Update(func(tx *bolt.Tx) error {
		b := tx.Bucket(self.patterns)
		local_message := strings.Join(append(places, password, ts), ":")
		err := b.Put([]byte(id), []byte(local_message))
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
	var local_message string
	self.db.View(func(tx *bolt.Tx) error {
		local_message = string(tx.Bucket(self.patterns).Get([]byte(id)))
		return nil
	})
	if local_message == "" {
		return ""
	}
	local_messages := strings.Split(local_message, ":")
	places, password, ts := local_messages[:len(local_messages)-2], local_messages[len(local_messages)-2], local_messages[len(local_messages)-1]
	good_places, pattern := receive_message(places, id, ts)
	self.db.Update(func(tx *bolt.Tx) error {
		p := tx.Bucket(self.places)
		for _, place := range good_places {
			db_place := []byte(place)
			tries, _ := strconv.Atoi(string(p.Get(db_place)))
			p.Put(db_place, []byte(strconv.Itoa(tries+1)))
		}
		return nil
	})
	return decode_pattern(pattern, password)
}
