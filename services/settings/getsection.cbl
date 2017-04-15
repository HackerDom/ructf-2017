       identification division.
       program-id. get-section.

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
           02 param-name picture x(20).
           02 filler picture x(933).
         01 result.
           02 rcode picture x(2).
           02 result-count picture 9.
           02 results occurs 9.
             03 result-container.
               04 rparam-name picture x(20).
               04 rparam-value picture x(85).
           02 filler picture x(76).
         01 result-length binary-long unsigned.

       procedure division 
         using argc, argv, result, result-length 
         returning need-more.
       start-get-section.
           if argc is less than 80
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

           perform 
             varying ind 
               from 1 by 1 until ind is greater than api-keys-count
             if skey is equal to api-key(ind)
               perform get-data
               goback
             end-if
           end-perform

           move 'na' to rcode
           move 2 to result-length.

       get-data.
           move 'ok' to rcode
           move zero to result-count
           move 3 to result-length

           move section-name to ssection-name
           move param-name to sparam-name
           perform forever
             if result-count is equal to 9
               goback
             end-if

             start settings-db 
               key is greater than composite-key
               invalid key
                 goback
             end-start

             read settings-db record 
               at end goback 
             end-read
             if ssection-name is not equal to section-name
               goback
             end-if

             add 1 to result-count end-add
             move sparam-name to rparam-name(result-count)
             move sparam-value to rparam-value(result-count)
             add function byte-length(result-container(result-count))
               to result-length
             end-add

           end-perform.


       end program get-section.

