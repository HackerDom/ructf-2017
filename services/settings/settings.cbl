       identification division.
       program-id. echoserver.

       environment division.
       input-output section.
       file-control.
         select optional keyvalue assign to external 'db.dat'
           organization is indexed
           access mode is random
           record key is name
           lock mode is automatic
           sharing with all other.
         select random-dev assign to external '/dev/urandom'.

       data division.
       file section.
         fd keyvalue is external.
         01 ssection.
           02 name picture x(40).
           02 api-keys occurs 9 times.
             03 api-key picture x(80).
           02 api-keys-count picture 9.
           02 state picture x(40).
         fd random-dev is external.
         01 buffer picture x(80).

       working-storage section.
         01 server-descriptor binary-int.
         01 port-binary binary-short unsigned.
       procedure division.
       start-echo-server.
           accept port-binary from argument-value end-accept
           open i-o keyvalue
           open input random-dev
           call 'perform-server-descriptor' using
             by reference port-binary
             by reference server-descriptor
           end-call
           call 'start-handling' using
             by reference server-descriptor
           end-call.
       end program echoserver.
