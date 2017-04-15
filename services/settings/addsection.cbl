       identification division.
       program-id. add-section.

       environment division.
       input-output section.
       file-control.
         copy sectiondb.

       data division.
       file section.
         copy sectionrecord.

       working-storage section.
       01 need-more picture 9.
       77 default-api-key picture x(360) value all '*'.

       linkage section.
       01 argc binary-long unsigned.
       01 argv.
         02 section-name picture x(20).
         02 filler picture x(993).
       01 result.
         02 rcode picture x(2).
         02 new-api-key picture x(40).
         02 filler picture x(982).
       01 result-length binary-long unsigned.

       procedure division 
         using argc, argv, result, result-length 
         returning need-more.
       start-add-section.
            if argc is less than 20
              move 1 to need-more
              goback
            else
              move zero to need-more
            end-if

            move section-name to name
            move default-api-key to api-keys
            move 1 to api-keys-count
            call 'random-string' using by reference api-keys end-call
            write ssection
              invalid key
                move 'fl' to rcode
                move 2 to result-length
                goback
            end-write

            move 'ok' to rcode
            move api-key(1) to new-api-key
            move 42 to result-length.

       end program add-section.
