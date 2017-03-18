       identification division.
       program-id. echoserver.
       data division.
       file section.
       working-storage section.
       01 server-descriptor binary-int.
       procedure division.
       start-echo-server.
           call 'perform-server-descriptor' using
             by reference 1234
             by reference server-descriptor
           end-call
           call 'start-handling' using
             by reference server-descriptor
           end-call.
       end program echoserver.
