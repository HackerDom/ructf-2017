       identification division.
       program-id. tune-socket.

       data division.
       working-storage section.
       01 flags  binary-int.

       77 SOL_SOCKET binary-int value 1.
       77 SO_REUSEADDR binary-int value 2.
       77 YES binary-int value 1.

       77 F_GETFL binary-int value 3.
       77 F_SETFL binary-int value 4.
       77 O_NONBLOCK binary-int value 2048.

       77 SETSOCKOPT_ERROR picture x(64) value 
                                       "server call 'setsockopt' filed".
       77 GET_ERROR picture x(64) value 
                                  "server call 'fcntl(F_GETFL)' failed".
       77 SET_ERROR picture x(64) value 
                                  "server call 'fcntl(F_SETFL)' failed".

       linkage section.
       01 fdesc binary-int.

       procedure division using fdesc.
      * TODO don't stop run if fail for peer 
       start-tune-socket.
           call 'setsockopt' using
             by value fdesc
             by value SOL_SOCKET
             by value SO_REUSEADDR
             by reference YES
             by value function length(YES)
           end-call
           if return-code is less than zero
             call 'log-error' using
               by content SETSOCKOPT_ERROR
             end-call
           end-if

           call 'fcntl' using
             by value fdesc
             by value F_GETFL
             by value 0
             returning flags
           end-call
           if return-code is less than zero
             call 'log-error' using
               by content GET_ERROR 
             end-call
           end-if

           call 'or' using
             by value flags
             by value O_NONBLOCK
             returning flags
           end-call

           call 'fcntl' using
             by value fdesc
             by value F_SETFL
             by value flags
           end-call
           if return-code is less than zero
             call 'log-error' using
               by content SET_ERROR
             end-call
           end-if
           goback.

       end program tune-socket.
