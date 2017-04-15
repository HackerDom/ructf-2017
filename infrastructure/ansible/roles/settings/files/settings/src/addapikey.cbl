       identification division.
       program-id. add-apikey.

       environment division.
       input-output section.
       file-control.
         copy sectiondb.

       data division.
       file section.
         copy sectionrecord.

       working-storage section.
         01 need-more picture 9.
         01 current-key-index picture 99.

         77 default-api-key picture x(40) value all '*'.

       linkage section.
         01 argc binary-long unsigned.
         01 argv.
           02 section-name picture x(20).
           02 current-api-key picture x(40).
           02 new-key picture x(40).
           02 filler picture x(913).
         01 result.
           02 rcode picture x(2).
           02 filler picture x(1022).
         01 result-length binary-long unsigned.

       procedure division 
         using argc, argv, result, result-length 
         returning need-more.
       start-api--key.
            if argc is less than 100
              move 1 to need-more
              goback
            else
              move zero to need-more
            end-if

            move section-name to name
            read sections-db record
              invalid key
                move 'bn' to rcode
                move 2 to result-length
                goback
            end-read

            if api-keys-count is equal to 9
              move 'mk' to rcode
              move 2 to result-length
              goback
            end-if
        
            perform
              varying current-key-index
                from 1 by 1 until current-key-index is greater than 9
              if current-api-key is equal to api-key(current-key-index) and current-api-key is not equal to default-api-key
                add 1 to api-keys-count end-add
                move new-key to api-key(api-keys-count)
                rewrite ssection
                  invalid key
                    move 'fl' to rcode
                    move 2 to result-length
                    goback
                end-rewrite
                move 'ok' to rcode
                move 2 to result-length
                goback
              end-if
            end-perform

            move 'na' to rcode
            move 2 to result-length.

       update-section.
       end program add-apikey.
