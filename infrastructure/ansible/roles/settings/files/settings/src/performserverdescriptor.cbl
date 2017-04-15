       identification division.
       program-id. perform-server-descriptor.

       data division.
       working-storage section.

       01 server-address.
           03  server-family binary-short unsigned.
           03  server-port binary-short unsigned.
           03  server-ip-address binary-long unsigned.
           03  filler picture x(8) value low-values.

       77 AF_INET binary-short unsigned value 2.
       77 SOCK_STREAM binary-short unsigned value 1.

       77 SOCKET_ERROR picture x(64) value "server call 'socket' filed".
       77 BIND_ERROR picture x(64) value "server call 'bind' failed".
       77 LISTEN_ERROR picture x(64) value 
                                          "server call 'listen' failed".
       77 add_poll_error picture x(64) value 
                                         "server call 'addread' failed".


       77 queue-length binary-char value 2.

       linkage section.
       01 port binary-short unsigned.
       01 server-descriptor binary-int.
       01 command-ip-address binary-int unsigned.

       procedure division
         using command-ip-address, port, server-descriptor.
       start-perform-server.

           call 'socket' using
               by value AF_INET
               by value SOCK_STREAM
               by value 0
               giving server-descriptor
           end-call
           if return-code is less than zero
             call 'logerror' using
               by content SOCKET_ERROR
               by content 1
             end-call
           end-if

          call 'tune-socket' using
             by reference server-descriptor
             by content 1
           end-call

           call 'htons' using
             by value port
             giving server-port
           end-call

           move AF_INET to server-family
           move command-ip-address to server-ip-address

           call 'bind' using
             by value server-descriptor
             by reference server-address
             by value function byte-length(server-address)
           end-call
           if return-code is less than zero
             call 'logerror' using
               by content BIND_ERROR 
               by content 1
             end-call
           end-if

           call 'listen' using
             by value server-descriptor
             by value queue-length
           end-call
           if return-code is less than zero
             call 'logerror' using
               by content LISTEN_ERROR 
               by content 1
             end-call
           end-if

          call 'addRead' using
             by value server-descriptor
           end-call
           if return-code is less than zero
             call 'logerror' using
               by content ADD_POLL_ERROR
               by content 1
             end-call
           end-if.
       end program perform-server-descriptor.
