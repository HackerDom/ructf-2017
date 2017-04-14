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
         01 admin-descriptor binary-int.
         01 admin-port binary-short unsigned.

         77 INIT_POLL_ERROR picture x(64) value
                                        "server call 'initPoll' failed".

       procedure division.
       start-echo-server.
           accept port-binary from argument-value end-accept
           accept admin-port from argument-value end-accept
           open i-o sections-db
           open input random-dev
           open i-o settings-db
           call 'initPoll' end-call
           if return-code is less than zero
             call 'logerror' using
               by content INIT_POLL_ERROR
               by content 1
             end-call
           end-if
           call 'perform-server-descriptor' using
             by content 0
             by reference port-binary
             by reference server-descriptor
           end-call
           call 'perform-server-descriptor' using
             by content 16777343
             by reference admin-port
             by reference admin-descriptor
           end-call
           call 'start-handling' using
             by reference server-descriptor
             by reference admin-descriptor
           end-call.
       end program settings.
