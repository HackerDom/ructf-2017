package main

import (
	"bytes"
	"encoding/binary"
	"math/rand"
)

func strInSlice(k string, list []string) bool {
	for _, b := range list {
		if b == k {
			return true
		}
	}
	return false
}

type Choice struct {
	Key    string
	Weight int
}

func randSlice(list []Choice, max_num int) chan string {
	slice := make(chan string)
	var choice []string

	go func() {
		for {
			if len(choice) == len(list) {
				break
			}
			r := rand.Intn(max_num)
			for _, c := range list {
				r -= c.Weight
				if r < 0 && !strInSlice(c.Key, choice) {
					slice <- c.Key
					choice = append(choice, c.Key)
					break
				}
			}
		}
		close(slice)
	}()
	return slice
}

func randString(n int) string {
	const (
		anum          = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
		letterIdxBits = 6
		letterIdxMask = 1<<letterIdxBits - 1
		letterIdxMax  = 63 / letterIdxBits
	)
	b := make([]byte, n)
	for i, cache, remain := n-1, rand.Int63(), letterIdxMax; i >= 0; {
		if remain == 0 {
			cache, remain = rand.Int63(), letterIdxMax
		}
		if idx := int(cache & letterIdxMask); idx < len(anum) {
			b[i] = anum[idx]
			i--
		}
		cache >>= letterIdxBits
		remain--
	}

	return string(b)
}

func bytesToU32(b []byte) []uint32 {
	var r []uint32
	if len(b)%4 != 0 {
		b = append(make([]byte, 4-len(b)%4), b...)
	}
	for i := 0; i < len(b); i += 4 {
		r = append(r, binary.BigEndian.Uint32(b[i:i+4]))
	}
	if len(r)%2 > 0 {
		r = append(r, uint32(0))
	}
	return r
}

func strToU32(s string) []uint32 {
	return bytesToU32([]byte(s))
}

func u32ToString(a []uint32) string {
	return string(u32ToBytes(a))
}

func u32ToBytes(a []uint32) []byte {
	buf := make([]byte, len(a)*4)
	for i, v := range a {
		binary.BigEndian.PutUint32(buf[i*4:], v)
	}
	return bytes.Trim(buf, "\x00")
}
