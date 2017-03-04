package main

import (
	"encoding/hex"
	"log"
	"strconv"
	"strings"
	"time"
)

func create_pattern(message string) (string, string, string) {
	ts := strconv.FormatInt(time.Now().Unix(), 16)
	password := randString(16)
	key := strToU32(password)
	btext := strToU32(":" + message + "pattern")
	var upattern []uint32
	for i := 0; i < len(btext); i += 2 {
		l, r := b_enc(btext[i], btext[i+1], key)
		upattern = append(upattern, l, r)
	}
	pattern := hex.EncodeToString(u32ToBytes(upattern))
	return pattern, password, ts
}

func decode_pattern(pattern, password string) string {
	key := strToU32(password)
	bpattern, err := hex.DecodeString(pattern)
	if err != nil {
		return err.Error()
	}
	btext := bytesToU32(bpattern)
	var upattern []uint32
	for i := 0; i < len(btext); i += 2 {
		l, r := b_dec(btext[i], btext[i+1], key)
		upattern = append(upattern, l, r)
	}
	message := u32ToString(upattern)
	log.Print(message, " - ", pattern)
	return strings.TrimPrefix(strings.TrimSuffix(message, "pattern"), ":")
}

func b_enc(v0, v1 uint32, k []uint32) (uint32, uint32) {
	delta := uint32(0x9e3779b9)
	v0 += (v1 << 4) ^ (k[0] << 4) ^ (v1 + delta) ^ (v1 >> 5) ^ (k[2] >> 5)
	v1 += (v0 << 4) ^ (k[1] << 4) ^ (v0 + delta) ^ (v0 >> 5) ^ (k[3] >> 5)
	return v0, v1
}

func b_dec(v0, v1 uint32, k []uint32) (uint32, uint32) {
	delta := uint32(0x9e3779b9)
	v1 -= (v0 << 4) ^ (k[1] << 4) ^ (v0 + delta) ^ (v0 >> 5) ^ (k[3] >> 5)
	v0 -= (v1 << 4) ^ (k[0] << 4) ^ (v1 + delta) ^ (v1 >> 5) ^ (k[2] >> 5)
	return v0, v1
}
