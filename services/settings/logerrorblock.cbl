       identification division.
       program-id. log-error-nonblock.

       data division.
       working-storage section.
       01 errno binary-char unsigned.
       01 errno-name picture x(16).
       01 errno-message picture x(64).
       01 need-close picture 9.

       77 EAGAIN picture x(16) value 'EAGAIN'.
       77 ENOTBLK picture x(16) value 'ENOTBLK'.
       77 NL picture x value x'0a'.

       linkage section.
       01 error-message picture x(64).

       procedure division using error-message returning need-close.
       start-log-error.
           call 'errnomessage' using
             by reference errno errno-name errno-message
           end-call
           display NL error-message end-display
           display errno space errno-name errno-message end-display
           if errno-name is equal to EAGAIN 
               or errno-name is equal to ENOTBLK
             move 0 to need-close
           else
             move 1 to need-close
           end-if
           display need-close end-display.

 
       end program log-error-nonblock.
