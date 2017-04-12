       identification division.
       program-id. fix-section.

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
           02 name picture x(40).
           02 api-keys occurs 9 times.
             03 api-key picture x(80).
           02 api-keys-count picture 9.
           02 state picture x(40).

       working-storage section.
         01 need-more picture 9.
         01 ind picture 9.
         01 x picture 9.
         01 y picture 99.
         01 z picture 99.
         01 tmp picture 999.

       linkage section.
         01 argc binary-long unsigned.
         01 argv.
           02 section-name picture x(40).
           02 skey picture x(80).
           02 card occurs 8 times.
             03 nl picture x.
             03 ln picture x(80).
           02 filler picture x(245).
         01 result.
           02 rcode picture x(2).
           02 rstate picture x(40).
           02 filler picture x(982).
         01 result-length binary-long unsigned.
 
       procedure division 
         using argc, argv, result, result-length 
         returning need-more.
       start-fix-section.
           if argc is less than 768
             move 1 to need-more
             goback
           else
             move zero to need-more
           end-if

           perform
             varying x from 1 by 1 until x is greater than 8
             if nl(x) is not equal to x'0a'
               move 'bp' to rcode
               move 2 to result-length
               goback
             end-if
             perform
               varying y from 1 by 1 until y is greater than 80
               if ln(x)(y:1) is not equal to ' ' 
                   and ln(x)(y:1) is not equal to '*'
                 move 'bp' to rcode
                 move 2 to result-length
                 goback
               end-if
             end-perform
           end-perform

           move section-name to name
           read keyvalue record
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
           move 1 to x y
           perform
             varying z from 1 by 1 until z is greater than 40
             if state(z:1) is less than x'37'
               add 3 to x end-add
               if x is greater than 8
                 subtract 8 from x end-subtract
               end-if
               multiply function ord(state(z:1)) by y end-multiply
               move function mod(y, 80) to y
               if y is equal to zero
                 move 80 to y
               end-if
               if ln(x)(y:1) is equal to ' '
                 move x to tmp
                 multiply y by tmp end-multiply
                 move function char(tmp) to state(z:1)
               else
                 move function ord(state(z:1)) to tmp
                 add x to tmp end-add
                 add y to tmp end-add
                 if tmp is greater than 256
                   subtract 256 from tmp end-subtract
                 end-if
                 move function char(tmp) to state(z:1)
               end-if
             end-if
           end-perform
           move 1 to z
           perform
             varying x from 1 by 1 until x is greater than 8
             perform
               varying y from 1 by 1 until y is greater than 80
               if ln(x)(y:1) is equal to '*'
                 add y to z end-add
                 multiply x by z end-multiply
                 move function mod(z, 40) to z
                 if z is equal to zero
                   move 40 to z
                 end-if
                 move function ord(state(z:1)) to tmp
                 subtract 257 from tmp end-subtract
                 move function ord(tmp) to state(z:1)
               end-if
             end-perform
           end-perform

           rewrite ssection
             invalid key
               move 'fl' to rcode
               move 2 to result-length
               goback
           end-rewrite

           move 'ok' to rcode
           move state to rstate
           move 42 to result-length.

       end program fix-section.
