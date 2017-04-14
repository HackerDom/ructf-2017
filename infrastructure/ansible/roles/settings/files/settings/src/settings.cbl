       identification division.
       program-id. settings.

       environment division.
       input-output section.
       file-control.
         copy sectiondb.
         copy settingdb.
         select random-dev assign to external '/dev/urandom'.

       data division.
       file section.
         copy sectionrecord.
         copy settingrecord.

         fd random-dev is external.
         01 buffer picture x(80).

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
