# Capter

* golang JSON-RPC server (capter)
* shared key-value (capterka)

## Legend

### General

There is a need, while process of planet research and terraforming, to send some chemical elements, soil samples and so on to different places on the planet. So, for the purity of experiment, these places must be chosen randomly, but weighted with their availability for living.
That is how "Cosmic Automatic Pattern Transmitter-Exchanger-Receiver" has been developed.

## Vulnerabilities

There are two vulns in the service, which partly connected (one vuln can simplify using of another). Here they are:

### LIST

> Simple REST-API vuln in Capterca
> It needs to know some common HTTP methods and luck, or in another way - Go binary reverse =)

There are some HTTP methods in REST protocol in Capterca (key-value storage), but main entrypoint for them is OPTIONS http method.

So, if you ask service which methods it could handle, it honestly show you:

    Available methods: {GET|POST|LIST|OPTIONS|LEN}

Wow! It has LIST method, which can return to you list of all keys on the service. But there is a little difficulty - service needs query parameter: `key` (that's why I mean luck or reverse needed)

If you understand, that Capter send encrypted messages by key: `$timestamp-$short_id`, it would simple to get list of last flag keys:
`curl -XLIST http://10.60.N.1:8081/?key=58f359` (first 6 chars of hex of timestamp)

Attack:

Get list of unique short ids from all capterca. For each `$short_id` you need to ask Capter about flag (with concatenating one of 5 words - types of message).

Defence:

It is enough to use one of:
1. Generate internal key name without flag_id, or even timestamp.
2. Patch capterca binary (or use reverse proxy) to disallow using LIST method.

### Crypto

>Simplified cryptography

Service use simplified version of Tiny Encryption Algorithm, where:
1. Number of rounds is 1
2. All operations replaced by XOR

That's why, instead of using 16 chars password, it uses just two uint32 numbers, and known plain text (message type). It is very simple to get these two uint32 by using that plain text. (you can see it in sploits/capter/crypto/sploit.go in repository)

Attack:

1. You can get all encrypted messages from your local capterca database (it is almost just a text file on disk, specially db log). After that, decrypt messages and get flags.
2. If you can use previous vuln (LIST), you don't need to generate so many requests as in simple LIST attack, but just send GET /?id=ID to capterca and decrypt it.

Defence:

Just use another cryptography, for example, more rounds, different operations, or another algorythm at all.