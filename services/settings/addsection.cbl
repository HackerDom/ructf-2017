       identification division.
       program-id. add-section.

       environment division.
       input-output section.
       file-control.
         select optional keyvalue assign to external 'db.dat'
           organization is indexed
           access mode is random
           record key is name
           lock mode is automatic
           sharing with all other.

       data division.
       file section.
         fd keyvalue is external.
         01 ssection.
           02 name picture x(13).
           02 api-keys occurs 9 times.
             03 api-key picture x(20).
           02 api-keys-count picture 9.

       working-storage section.
       01 need-more picture 9.

       linkage section.
       01 argc binary-long unsigned.
       01 argv.
         02 section-name picture x(13).
         02 filler picture x(1000).
       01 result.
         02 state picture x(2).
         02 new-api-key picture x(20).
         02 filler picture x(1002).
       01 result-length binary-long unsigned.

       procedure division 
         using argc, argv, result, result-length 
         returning need-more.
       start-add-section.
            if argc is less than 13
              move 1 to need-more
              goback
            else
              move zero to need-more
            end-if

            move section-name to name
            move 1 to api-keys-count
            call 'random-string' using by reference api-key(1) end-call
            write ssection
              invalid key
                move 'fl' to state
                move 2 to result-length
                goback
            end-write
            unlock keyvalue
      *      call 'cob_sync' using
      *        by reference keyvalue
      *        returning omitted
      *      end-call

            move 'ok' to state
            move api-key(1) to new-api-key
            move 22 to result-length.


       end program add-section.
