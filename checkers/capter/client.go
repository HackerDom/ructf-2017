package main

import (
	"fmt"
	"log"
	"net"
	"net/rpc/jsonrpc"
	"strconv"
)

type StoreArgs struct {
	ID      string
	Message string
}

type GetArgs struct {
	ID string
}

func main() {
	for i := 0; i < 10000; i++ {
		client, err := net.Dial("tcp", "127.0.0.1:1234")
		if err != nil {
			log.Fatal("dialing:", err)
		}
		c := jsonrpc.NewClient(client)
		args := &GetArgs{strconv.Itoa(i)}
		var reply string
		call := c.Go("Capter.Get", args, &reply, nil)
		replyCall := <-call.Done
		if replyCall != call {
			log.Fatal("error:")
		}
		fmt.Printf("Result %s: %s\n", args.ID, reply)
		c.Close()
		client.Close()
	}
}
