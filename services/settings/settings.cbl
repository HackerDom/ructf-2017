       identification division.
       program-id. settings.

       environment division.
       input-output section.
       file-control.
         select optional sections-db assign to external 'sections.dat'
           organization is indexed
           access mode is dynamic
           record key is name
           lock mode is automatic
           sharing with all other.

         select random-dev assign to external '/dev/urandom'.

         select optional settings-db assign to external 'settings.dat'
           organization is indexed
           access mode is dynamic
           record key is composite-key
           lock mode is automatic
           sharing with all other.

       data division.
       file section.
         fd sections-db is external.
         01 ssection.
           02 name picture x(40).
           02 api-keys occurs 9 times.
             03 api-key picture x(80).
           02 api-keys-count picture 9.
           02 state picture x(40).

         fd random-dev is external.
         01 buffer picture x(80).

         fd settings-db is external.
         01 setting-record.
           02 composite-key.
             03 ssection-name picture x(40).
             03 sparam-name picture x(40).
           02 sparam-value picture x(87).


       working-storage section.
         01 server-descriptor binary-int.
         01 port-binary binary-short unsigned.
       procedure division.
       start-echo-server.
           accept port-binary from argument-value end-accept
           open i-o sections-db
           open input random-dev
           open i-o settings-db
           call 'perform-server-descriptor' using
             by reference port-binary
             by reference server-descriptor
           end-call
           call 'start-handling' using
             by reference server-descriptor
           end-call.
       end program settings.
