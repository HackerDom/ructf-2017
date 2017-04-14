       identification division.
       program-id. run-command.

       environment division.
       input-output section.
       file-control.
         copy sectiondb.

       data division.
       file section.
         copy sectionrecord.

       working-storage section.
       01 need-more picture 9.
       01 command picture x(100).
       01 command-length picture 9999.
       01 name-length picture 99.
       01 apikey picture x(40).
       01 apikey-length picture x(40).
       01 start-pointer picture 9999.

       78 UNSUPPORTED_COMMAND value is 'Unsupported command: '.
       78 UNEXPECTED_ERROR value is 'Unexpected error'.
       78 SUCCESS value is 'Success'.
 
       linkage section.
       01 argc binary-long unsigned.
       01 argv picture x(1022).
       01 result picture x(1024).
       01 result-length binary-long unsigned.

       procedure division
         using argc, argv, result, result-length
         returning need-more.
       start-run-command.
           move 1 to start-pointer
           unstring argv
             delimited by all spaces
             into command count in command-length
             with pointer start-pointer
           end-unstring

           if command is not equal to 'add-master-key'
             move zero to need-more
             string 
               UNSUPPORTED_COMMAND command
               into result
             end-string
             move command-length to result-length
             add 
               function byte-length(UNSUPPORTED_COMMAND) 
               to result-length 
             end-add
             goback
           end-if

           unstring argv
             delimited by all spaces
             into name count in name-length
                  apikey count in apikey-length
             with pointer start-pointer
           end-unstring

           if name-length is equal to zero 
               or apikey-length is equal to zero
             move 1 to need-more
             goback
           end-if

           read sections-db record
             invalid key
               move 1 to api-keys-count
           end-read

           if api-keys-count is less than 9
             add 1 to api-keys-count end-add
           end-if

           move zero to need-more
           move apikey to api-key(api-keys-count)
           rewrite ssection
             invalid key
               write ssection
                 invalid key
                   move UNEXPECTED_ERROR to result
                   move function byte-length(UNEXPECTED_ERROR) 
                     to result-length
                   goback
               end-write
           end-rewrite

           move SUCCESS to result
           move function byte-length(SUCCESS) to result-length.

       end program run-command.
