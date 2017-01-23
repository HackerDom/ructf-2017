package main

import (
	"errors"
)

type StoreArgs struct {
	ID      string
	Message string
}

type GetArgs struct {
	ID string
}

func (self *Capter) Put(args *StoreArgs, reply *string) error {
	if err := self.store(args.ID, args.Message); err != nil {
		return err
	}
	*reply = "Message stored"
	return nil
}

func (self *Capter) Get(args *GetArgs, reply *string) error {
	*reply = self.get(args.ID)
	if reply == nil {
		return errors.New("Not found")
	}
	return nil
}
