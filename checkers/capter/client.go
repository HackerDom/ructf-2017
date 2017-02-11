package main

import (
	"fmt"
	"log"
	"net"
	"net/rpc/jsonrpc"
	"strconv"
	"sync"
)

type StoreArgs struct {
	ID      string
	Message string
}

type GetArgs struct {
	ID string
}

func store(n int, wg *sync.WaitGroup) {
	defer wg.Done()
	client, err := net.Dial("tcp", "127.0.0.1:1234")
	if err != nil {
		log.Fatal("dialing:", err)
	}
	c := jsonrpc.NewClient(client)
	args := &StoreArgs{strconv.Itoa(n), "Hello"}
	var reply string
	call := c.Go("Capter.Put", args, &reply, nil)
	replyCall := <-call.Done
	if replyCall != call {
		log.Fatal("error:")
	}
	fmt.Printf("Result %s: %s\n", args.ID, reply)
	c.Close()
	client.Close()
}

func main() {
	var wg sync.WaitGroup
	// wg.Add(1)
	// store(0, &wg)
	for i := 0; i < 10000; i++ {
		wg.Add(10)
		for j := 0; j < 10; j++ {
			go store(i+j, &wg)
		}
		wg.Wait()
	}
}
