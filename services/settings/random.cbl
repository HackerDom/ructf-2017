       identification division.
       program-id. random-string.

       environment division.
       input-output section.
       file-control.
         select random-dev assign to external '/dev/urandom'.
       
       data division.
       file section.
         fd random-dev is external.
         01 buffer picture x(40).
       
       working-storage section.
         01 ind picture 99.
         01 chr picture 999.

         77 alph picture x(62) value 
                                                             '0123456789
      -                                      'abcdefghijklmnopqrstuvwxyz
      -       'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.
       linkage section.
         01 result picture x(40).

       procedure division using result.
       start-rand.
         read random-dev record end-read
         perform 
           varying ind from 1 by 1 until ind is greater than 40
           move function ord(buffer(ind:1)) to chr
           move function mod(chr, 62) to chr
           add 1 to chr end-add
           move alph(chr:1) to result(ind:1)
         end-perform.

       end program random-string.
