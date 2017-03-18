       identification division.
       program-id. start-handling.

       data division.
       working-storage section.
       01 fdesc binary-int.
       01 event binary-int.

       01 peer-descriptor binary-int.
       01 peer-address.
         03 peer-family binary-short unsigned.
         03 peer-port binary-short unsigned.
         03 peer-ip-address binary-int unsigned.
         03 filler picture x(8) value low-values.
       01 peer-address-length binary-short unsigned.

       01 buffers-pool.
         02 buffers occurs 1024 times indexed by buffer-number.
           03 buffer picture x(65536).
           03 buffer-length binary-long unsigned.
           03 buffer-sended binary-long unsigned.
           03 socket binary-int value -1.

       01 flag binary-int unsigned.
       01 need-close picture 9.

       77 MSG_NOSIGNAL binary-int value 16384.

       77 ADD_POLL_ERROR picture x(64) value 
                                         "server call 'addread' failed".
       77 ACCEPT_ERROR picture x(64) value 
                                          "server call 'accept' failed".
       77 RECV_ERROR picture x(64) value "server call 'recv' failed".
       77 SEND_ERROR picture x(64) value "server call 'send' failed".

       77 NL picture x value x'0a'.

       77 POLLIN binary-int unsigned value 1.
       77 POLLOUT binary-int unsigned value 4.

       linkage section.
       01 server-descriptor binary-int.

       procedure division using server-descriptor.
       start-handling.
           perform process-event forever.

       process-event.
           call 'getEvent' using
             by reference fdesc
             by reference event
           end-call
           if fdesc is equal to server-descriptor
             perform add-new-client
             exit paragraph
           end-if.
           call 'and' using
             by value event
             by value POLLIN
             returning flag 
           end-call
      D    display 'event and POLLIN = ' flag end-display
           if flag is equal to POLLIN
             perform recv
             exit paragraph
           end-if
           call 'and' using
             by value event
             by value POLLOUT
             returning flag
           end-call
      D    display 'event and POLLOUT = ' flag end-display
           if flag is equal to POLLOUT
             perform send
             exit paragraph
           end-if
      D    display 'strange event ' event end-display
           .


       add-new-client.
           perform forever
             move function length(peer-address) to peer-address-length
             call 'accept' using
               by value server-descriptor
               by reference peer-address
               by reference peer-address-length
               giving peer-descriptor
             end-call
             if return-code is less than zero
               call 'log-error-nonblock' using
                 by content ACCEPT_ERROR
                 returning need-close
               end-call
               exit perform
             end-if

             call 'tune-socket' using
               by reference peer-descriptor
             end-call

             call 'addRead' using
               by value peer-descriptor
             end-call
             if return-code is less than zero
               call 'log-error' using
                 by content ADD_POLL_ERROR
                 by content 0
               end-call
             end-if

      D      display 'new connection from ' 
      D        peer-ip-address ':' peer-port end-display

           end-perform.

       recv.
      D    display 'recv fdesc:' fdesc end-display
           call 'removeRead' using 
             by value fdesc
           end-call
           set buffer-number to 1
           search buffers 
             when socket(buffer-number) is equal to -1
             perform recv-to-buffer
           end-search.


       recv-to-buffer.
           move spaces to buffer(buffer-number)
      D    display 'buffer num: ' buffer-number ' buffer size: ' 
      D      function length(buffer(buffer-number)) end-display
           call 'recv' using 
             by value fdesc
             by reference buffer(buffer-number)
             by value function length(buffer(buffer-number))
             by value 0
           end-call
           evaluate return-code
             when -1
               call 'log-error-nonblock' using
                 by content RECV_ERROR
                 returning need-close
               end-call
               if need-close is greater than zero
                 perform close-connection
               end-if
             when 0
               perform close-connection
             when other
               set buffer-length(buffer-number) to return-code
               set socket(buffer-number) to fdesc
               set buffer-sended(buffer-number) to 1
           end-evaluate
           if buffer-length(buffer-number) is less than or equal to zero
             call 'addRead' using
               by value fdesc
             end-call
      D      display 'add read ' fdesc end-display
           else
             call 'addWrite' using
               by value fdesc
             end-call
      D      display 'add write ' fdesc end-display
           end-if.

       send.
      D    display 'send to ' fdesc end-display
           set buffer-number to 1
           search buffers
             when socket(buffer-number) is equal to fdesc
             perform send-buffer
           end-search.


       send-buffer.
      D    display 'buffer num: ' buffer-number ' buffer size: ' 
      D      buffer-length(buffer-number) end-display
           call 'send' using
             by value fdesc
             by reference 
               buffer(buffer-number)(
                 buffer-sended(buffer-number)
                   :buffer-length(buffer-number)
               )
             by value buffer-length(buffer-number)
             by value MSG_NOSIGNAL
           end-call
           if return-code is equal to -1
             call 'log-error-nonblock' using
               by content SEND_ERROR
               returning need-close
             end-call
             if need-close is greater than zero
               perform close-connection
             end-if
           end-if
           add return-code to buffer-sended(buffer-number) end-add
           subtract 
             return-code from buffer-length(buffer-number) 
           end-subtract
           if buffer-length(buffer-number) is less than or equal to zero
             move -1 to socket(buffer-number)
             call 'removeWrite' using
               by value fdesc
             end-call
      D      display 'remove write ' fdesc end-display
             call 'addRead' using
               by value fdesc
             end-call
      D      display 'add read ' fdesc end-display
           end-if.

       close-connection.
           set socket(buffer-number) to -1
           call 'close' using
             by value fdesc
           end-call.

       end program start-handling.
