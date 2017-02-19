package main

func create_pattern(id, message string) ([]byte, []byte) {
	return []byte(id + ":" + message), []byte("password")
}
