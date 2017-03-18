       identification division.
       program-id. perform-server-descriptor.

       data division.
       working-storage section.

       01 server-address.
           03  server-family binary-short unsigned.
           03  server-port binary-short unsigned.
           03  server-ip-address binary-int unsigned.
           03  filler picture x(8) value low-values.

       77 AF_INET binary-short unsigned value 2.
       77 SOCK_STREAM binary-short unsigned value 1.

       77 SOCKET_ERROR picture x(64) value "server call 'socket' filed".
       77 BIND_ERROR picture x(64) value "server call 'bind' failed".
       77 LISTEN_ERROR picture x(64) value 
                                          "server call 'listen' failed".
       77 INIT_POLL_ERROR picture x(64) value 
                                        "server call 'initPoll' failed".
       77 add_poll_error picture x(64) value 
                                         "server call 'addread' failed".


       77 queue-length binary-char value 2.

       linkage section.
       01 port binary-short.
       01 server-descriptor binary-int.

       procedure division using port, server-descriptor.
       start-perform-server.
      D    display "port: ", port end-display

           call 'socket' using
               by value AF_INET
               by value SOCK_STREAM
               by value 0
               giving server-descriptor
           end-call
           if return-code is less than zero
             call 'log-error' using
               by content SOCKET_ERROR
               by content 1
             end-call
           end-if

      D    display "create socket: ", server-descriptor end-display

          call 'tune-socket' using
             by reference server-descriptor
             by content 1
           end-call

      D    display "tune socket" end-display

           call 'htons' using
             by value port
             giving server-port
           end-call

      D    display "binary port: ", server-port end-display

           move AF_INET to server-family
           move 0 to server-ip-address

           call 'bind' using
             by value server-descriptor
             by reference server-address
             by value function length(server-address)
           end-call
           if return-code is less than zero
             call 'log-error' using
               by content BIND_ERROR 
               by content 1
             end-call
           end-if

      D    display "bind" end-display

           call 'listen' using
             by value server-descriptor
             by value queue-length
           end-call
           if return-code is less than zero
             call 'log-error' using
               by content LISTEN_ERROR 
               by content 1
             end-call
           end-if

      D    display "start listen" end-display

           call 'initPoll' end-call
           if return-code is less than zero
             call 'log-error' using
               by content INIT_POLL_ERROR
               by content 1
             end-call
           end-if

           call 'addRead' using
             by value server-descriptor
           end-call
           if return-code is less than zero
             call 'log-error' using
               by content ADD_POLL_ERROR
               by content 1
             end-call
           end-if

      D    display "init polling" end-display

      *     perform forever
      *       perform accept-new
      *       perform response-all
      *     end-perform.

      *accept-new.
      *   move function length(peer-address) to peer-address-length
      *   call 'accept' using
      *     by value server-descriptor
      *     by reference peer-address
      *     by reference peer-address-length
      *     giving peer-descriptor
      *   end-call
      *   if return-code is equal to -1
      *     call 'errnomessage' using
      *       by reference errno errno-name errno-message
      *     end-call
      *     if
      *       errno-name is not equal to 'EAGAIN'
      *       and errno-name is not equal to 'EWOULDBLOCK'
      *         move "server call 'accept' failed" to abort-message
      *         perform abort-server
      *     end-if
      *
      *   end-if.


           goback.
       end program perform-server-descriptor.
