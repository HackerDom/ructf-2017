package main

import (
	"fmt"
	"log"
	"math/rand"
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

type TopArgs struct {
	Limit int
}

func store(n int) string {
	client, err := net.Dial("tcp", "127.0.0.1:1234")
	if err != nil {
		log.Fatal("dialing:", err)
	}
	c := jsonrpc.NewClient(client)
	id := strconv.Itoa(n) + "-" + strconv.Itoa(rand.Intn(1000))
	args := &StoreArgs{id, strconv.Itoa(rand.Intn(1000)+2000) + "92034824a48343e46280ec1330f=pattern"}
	var reply string
	call := c.Go("Capter.Put", args, &reply, nil)
	replyCall := <-call.Done
	if replyCall != call {
		log.Fatal("error:")
	}
	if call.Error != nil {
		fmt.Printf("Put %s failed: %s\n", args.ID, call.Error.Error())
		// } else {
		// fmt.Printf("Put %s: %s\n", args.ID, reply)
	}
	c.Close()
	client.Close()
	return id
}

func get(id string) {
	client, err := net.Dial("tcp", "127.0.0.1:1234")
	if err != nil {
		log.Fatal("dialing:", err)
	}
	c := jsonrpc.NewClient(client)
	args := &GetArgs{id}
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

func top(n int) {
	client, err := net.Dial("tcp", "127.0.0.1:1234")
	if err != nil {
		log.Fatal("dialing:", err)
	}
	c := jsonrpc.NewClient(client)
	args := &TopArgs{n}
	var reply string
	call := c.Go("Capter.Top", args, &reply, nil)
	replyCall := <-call.Done
	if replyCall != call {
		log.Fatal("error:")
	}
	if call.Error != nil {
		fmt.Printf("Top %s failed: %s\n", args.Limit, call.Error.Error())
	} else {
		fmt.Printf("Top %v: %v\n", args.Limit, reply)
	}
	c.Close()
	client.Close()
}

func store_get(n int, wg *sync.WaitGroup) {
	defer wg.Done()
	get(store(n))
}

func main() {
	var wg sync.WaitGroup
	// store_get(0, &wg)
	// top(5)
	for i := 0; i < 1000; i += 50 {
		wg.Add(50)
		for j := 0; j < 50; j++ {
			store_get(i+j, &wg)
		}
		wg.Wait()
	}
}
