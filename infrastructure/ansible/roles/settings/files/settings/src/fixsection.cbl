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
         01 ind picture 9.

       linkage section.
         01 argc binary-long unsigned.
         01 argv.
           02 section-name picture x(20).
           02 skey picture x(40).
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
             varying ind 
               from 1 by 1 until ind is greater than api-keys-count
             if skey is equal to api-key(ind)
               perform apply-patch
               goback
             end-if
           end-perform

           move 'na' to rcode
           move 2 to result-length.

       apply-patch.

           move section-name to ssection-name
           perform 
             varying ind 
               from 1 by 1 until ind is greater than patches-count
             move param-name(ind) to sparam-name
             move param-value(ind) to sparam-value
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
