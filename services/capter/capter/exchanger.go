package main

import (
	"errors"
	"log"
	"math/rand"
	"net"
	"net/rpc"
	"net/rpc/jsonrpc"
	"time"
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
	*reply = "Stored"
	return nil
}

func (self *Capter) Get(args *GetArgs, reply *string) error {
	*reply = self.get(args.ID)
	if reply == nil {
		return errors.New("Not found")
	}
	return nil
}

func main() {
	server := rpc.NewServer()
	server.Register(NewCapter())
	listener, e := net.Listen("tcp", ":1234")
	if e != nil {
		log.Fatal("listen error:", e)
	}
	for {
		if conn, err := listener.Accept(); err != nil {
			log.Fatal("accept error: " + err.Error())
		} else {
			log.Print("new connection established")
			rand.Seed(time.Now().Unix())
			go server.ServeCodec(jsonrpc.NewServerCodec(conn))
		}
	}
}
