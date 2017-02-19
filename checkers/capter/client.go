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
	if call.Error != nil {
		fmt.Printf("Put %s failed: %s\n", args.ID, call.Error.Error())
	} else {
		fmt.Printf("Put %s: %s\n", args.ID, reply)
	}
	c.Close()
	client.Close()
}

func get(n int, wg *sync.WaitGroup) {
	defer wg.Done()
	client, err := net.Dial("tcp", "127.0.0.1:1234")
	if err != nil {
		log.Fatal("dialing:", err)
	}
	c := jsonrpc.NewClient(client)
	args := &GetArgs{strconv.Itoa(n)}
	var reply string
	call := c.Go("Capter.Get", args, &reply, nil)
	replyCall := <-call.Done
	if replyCall != call {
		log.Fatal("error:")
	}
	if call.Error != nil {
		fmt.Printf("Get %s failed: %s\n", args.ID, call.Error.Error())
	} else {
		fmt.Printf("Get %s: %s\n", args.ID, reply)
	}
	c.Close()
	client.Close()
}

func main() {
	var wg sync.WaitGroup
	wg.Add(2)
	store(0, &wg)
	get(0, &wg)

	// for i := 100; i < 10000; i += 10 {
	// 	wg.Add(10)
	// 	for j := 0; j < 10; j++ {
	// 		go store(i+j, &wg)
	// 		wg.Add(1)
	// 		go get(i+j, &wg)
	// 	}
	// 	wg.Wait()
	// }
}
