package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"math/rand"
	"net"
	"net/http"
	"net/rpc/jsonrpc"
	"os"
	"strings"
	"time"
)

const (
	OK             = 101
	CORRUPT        = 102
	MUMBLE         = 103
	DOWN           = 104
	INTERNAL_ERROR = 110
)

func die(out, err string, code int) {
	if len(out) > 0 {
		fmt.Println(out)
	}
	if len(err) > 0 {
		fmt.Fprintln(os.Stderr, err)
	}
	os.Exit(code)
}

func capterCommand(hostname, command string, args interface{}) string {
	client, err := net.Dial("tcp", hostname+":1234")
	if err != nil {
		die("No connect", err.Error(), DOWN)
	}
	defer client.Close()
	c := jsonrpc.NewClient(client)
	defer c.Close()
	var reply string
	call := c.Go("Capter."+command, args, &reply, nil)
	replyCall := <-call.Done
	if replyCall != call {
		die("Where is my answer?", "replyCall != call", MUMBLE)
	}
	if call.Error != nil {
		die("Bad answer", call.Error.Error(), MUMBLE)
	}
	return reply
}

func check(hostname string) {
	reply := capterCommand(hostname, "Info", nil)
	fmt.Fprintln(os.Stderr, reply)

	client := &http.Client{Timeout: time.Second * 3}
	req, _ := http.NewRequest("LEN", "http://"+hostname+":8081", nil)
	resp, err := client.Do(req)
	if err != nil {
		die("C.A.P.T.E.R.C.A is down", err.Error(), DOWN)
	}
	defer resp.Body.Close()
	banswer, err := ioutil.ReadAll(resp.Body)
	answer := "C.A.P.T.E.R.C.A: " + string(bytes.TrimSpace(banswer))
	if resp.StatusCode != 200 {
		die("C.A.P.T.E.R.C.A bad answer", answer, MUMBLE)
	} else {
		fmt.Fprintln(os.Stderr, answer)
	}
	os.Exit(OK)
}

type StoreArgs struct {
	ID      string
	Message string
}

type GetArgs struct {
	ID string
}

func messageType() string {
	rand.Seed(time.Now().UnixNano())
	types := []string{
		"pattern",
		"Presult",
		"Nresult",
		"feedb3k",
		"quality",
	}
	return types[rand.Intn(5)]
}

func put(hostname, id, flag string) {
	message_type := messageType()
	args := &StoreArgs{id, flag + message_type}
	reply := capterCommand(hostname, "Put", args)
	if reply == "Stored" {
		die(id+"="+message_type, "", OK)
	}
	die("Put failed", reply, MUMBLE)
}

func get(hostname, id, flag string) {
	id_type := strings.Split(id, "=")
	if len(id_type) < 2 {
		die("Bad ID", id, INTERNAL_ERROR)
	}
	args := &GetArgs{id_type[0]}
	reply := capterCommand(hostname, "Get", args)
	if reply == flag+id_type[1] {
		die("", "", OK)
	}
	if len(reply) > 0 {
		die("Bad flag", reply, MUMBLE)
	}
	die("Flag not found", reply, CORRUPT)
}

func main() {
	if len(os.Args) < 2 {
		die("Our check system is drunk", "command not found", INTERNAL_ERROR)
	}
	command := os.Args[1]
	switch command {
	case "info":
		die("vulns: 1", "", OK)
	case "check":
		if len(os.Args) < 3 {
			die("Our check system is drunk", "host argument not found", INTERNAL_ERROR)
		}
		check(os.Args[2])
	case "put":
		if len(os.Args) < 5 {
			die("Our check system is drunk", "Not enough arguments", INTERNAL_ERROR)
		}
		put(os.Args[2], os.Args[3], os.Args[4])
	case "get":
		if len(os.Args) < 5 {
			die("Our check system is drunk", "Not enough arguments", INTERNAL_ERROR)
		}
		get(os.Args[2], os.Args[3], os.Args[4])
	}
}
