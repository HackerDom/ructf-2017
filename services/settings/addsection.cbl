       identification division.
       program-id. add-section.

       environment division.
       input-output section.
       file-control.
         select optional sections-db assign to external 'sections.dat'
           organization is indexed
           access mode is dynamic
           record key is name
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

       working-storage section.
       01 need-more picture 9.

       linkage section.
       01 argc binary-long unsigned.
       01 argv.
         02 section-name picture x(40).
         02 filler picture x(973).
       01 result.
         02 rcode picture x(2).
         02 new-api-key picture x(80).
         02 filler picture x(942).
       01 result-length binary-long unsigned.

       procedure division 
         using argc, argv, result, result-length 
         returning need-more.
       start-add-section.
            if argc is less than 40
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
                move 'fl' to rcode
                move 2 to result-length
                goback
            end-write

            move 'ok' to rcode
            move api-key(1) to new-api-key
            move 82 to result-length.

       end program add-section.
