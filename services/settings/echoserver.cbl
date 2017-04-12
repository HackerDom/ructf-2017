       identification division.
       program-id. echoserver.
       data division.
       file section.
       working-storage section.
       01 server-descriptor binary-int.
       01 port picture 9(5).
       01 port-binary binary-short unsigned.
       procedure division.
       start-echo-server.
           accept port from argument-value end-accept
           move port to port-binary
           display port-binary end-display
           call 'perform-server-descriptor' using
             by reference port-binary
             by reference server-descriptor
           end-call
           call 'start-handling' using
             by reference server-descriptor
           end-call.
       end program echoserver.
