       identification division.
       program-id. all-section.

       environment division.
       input-output section.
       file-control.
         copy sectiondb.

       data division.
       file section.
         copy sectionrecord.
         
       working-storage section.
         01 need-more picture 9.

       linkage section.
         01 argc binary-long unsigned.
         01 argv.
           02 section-name picture x(20).
           02 filler picture x(993).
         01 result.
           02 rcode picture x(2).
           02 result-count picture 99.
           02 results occurs 51.
             03 rsection-name picture x(20).
         01 result-length binary-long unsigned.

       procedure division 
         using argc, argv, result, result-length 
         returning need-more.
       start-all-section.
           if argc is less than 20
             move 1 to need-more
             goback
           else
             move zero to need-more
           end-if

           move 'ok' to rcode
           move zero to result-count
           move 4 to result-length
           move section-name to name
           start sections-db
             key is greater than name
             invalid key
               goback
           end-start

           perform forever
             if result-count is equal to 51
               goback
             end-if

             read sections-db record
               at end goback
             end-read

             add 1 to result-count end-add
             move name to rsection-name(result-count)
             add 20 to result-length end-add
          end-perform.

       end program all-section.
