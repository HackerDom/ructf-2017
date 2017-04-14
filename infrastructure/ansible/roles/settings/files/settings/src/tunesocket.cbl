       identification division.
       program-id. tune-socket.

       data division.
       working-storage section.
       01 flags  binary-int.
       01 is-success picture 9.

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
       01 need-abort picture 9.

       procedure division using fdesc, need-abort returning is-success.
       start-tune-socket.
           move 1 to is-success
           call 'setsockopt' using
             by value fdesc
             by value SOL_SOCKET
             by value SO_REUSEADDR
             by reference YES
             by value function length(YES)
           end-call
           if return-code is less than zero
             call 'logerror' using
               by content SETSOCKOPT_ERROR
               by value need-abort
             end-call
             move zero to is-success
             goback
           end-if

           call 'fcntl' using
             by value fdesc
             by value F_GETFL
             by value 0
             returning flags
           end-call
           if return-code is less than zero
             call 'logerror' using
               by content GET_ERROR 
               by value need-abort
             end-call
             move zero to is-success
             goback
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
             call 'logerror' using
               by content SET_ERROR
               by value need-abort
             end-call
             move zero to is-success
             goback
           end-if
           goback.

       end program tune-socket.
