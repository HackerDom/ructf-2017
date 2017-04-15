       identification division.
       program-id. fix-section.

       environment division.
       input-output section.
       file-control.
         copy sectiondb.
         copy settingdb.

       data division.
       file section.
         copy sectionrecord.
         copy settingrecord.

       working-storage section.
         01 need-more picture 9.
         01 current-key-index picture 99.
         01 patch-index picture 9.

         77 default-api-key picture x(40) value all '*'.

       linkage section.
         01 argc binary-long unsigned.
         01 argv.
           02 section-name picture x(20).
           02 current-api-key picture x(40).
           02 patches-count picture 9.
           02 patch occurs 9 times.
             03 param-name picture x(20).
             03 param-value picture x(85).
           02 filler picture x(7).
         01 result.
           02 rcode picture x(2).
           02 filler picture x(1022).
         01 result-length binary-long unsigned.
 
       procedure division 
         using argc, argv, result, result-length 
         returning need-more.
       start-fix-section.
            if argc is less than 61
              move 1 to need-more
              goback
            else
              move zero to need-more
            end-if

            if patches-count is equal to zero
              move 'ok' to rcode
              move 2 to result-length
              goback
            end-if

            move section-name to name
            read sections-db record
              invalid key
                move 'bn' to rcode
                move 2 to result-length
                goback
            end-read

            perform
              varying current-key-index
                from 1 by 1 until current-key-index is greater than 9
              if current-api-key is equal to api-key(current-key-index) and current-api-key is not equal to default-api-key
                perform apply-patch
                goback
              end-if
            end-perform

            move 'na' to rcode
            move 2 to result-length
            goback.

       apply-patch.

            move section-name to ssection-name
            perform
              varying patch-index
                from 1 by 1
                  until patch-index is greater than patches-count
              move param-name(patch-index) to sparam-name
              move param-value(patch-index) to sparam-value
              write setting-record
                invalid key
                  rewrite setting-record
                    invalid key
                      move 'fl' to rcode
                      move 2 to result-length
                  end-rewrite
              end-write
            end-perform

            move 'ok' to rcode
            move 2 to result-length.

       end program fix-section.
