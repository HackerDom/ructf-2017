package main

import (
	"bytes"
	"encoding/binary"
	"encoding/hex"
	"fmt"
	"os"
)

func bytesToU32(b []byte) []uint32 {
	var r []uint32
	for i := 0; i < len(b); i += 4 {
		r = append(r, binary.BigEndian.Uint32(b[i:i+4]))
	}
	if len(r) < 4 {
		r = append(r, make([]uint32, 4-len(r))...)
	}
	return r
}

func strToU32(s string) []uint32 {
	b := []byte(s)
	return bytesToU32(b)
}

func u32ToString(a []uint32) string {
	buf := make([]byte, len(a)*4)
	for i, v := range a {
		binary.BigEndian.PutUint32(buf[i*4:], v)
	}
	return string(bytes.Trim(buf, "\x00"))
}

func b_dec(v0, v1, k0, k1 uint32) (uint32, uint32) {
	delta := uint32(0x9e3779b9)
	v1 -= (v0 << 4) ^ k1 ^ (v0 + delta) ^ (v0 >> 5)
	v0 -= (v1 << 4) ^ k0 ^ (v1 + delta) ^ (v1 >> 5)
	return v0, v1
}

func main() {
	se := os.Args[1]
	btext := []uint32{0x3d706174, 0x7465726e} // =pattern
	epattern, _ := hex.DecodeString(se)
	etext := bytesToU32(epattern)
	delta := uint32(0x9e3779b9)
	last := len(etext) - 1
	prev := len(etext) - 2
	k1 := (etext[last] - btext[1]) ^ (etext[prev] << 4) ^ (etext[prev] + delta) ^ (etext[prev] >> 5)
	k0 := (etext[prev] - btext[0]) ^ (btext[1] << 4) ^ (btext[1] + delta) ^ (btext[1] >> 5)
	var p []uint32
	for i := 0; i < len(etext); i += 2 {
		x, y := b_dec(etext[i], etext[i+1], k0, k1)
		p = append(p, x, y)
	}
	fmt.Println(u32ToString(p))
}
