       identification division.
       program-id. log-error.

       data division.
       working-storage section.
       01 errno binary-char unsigned.
       01 errno-name picture x(16).
       01 errno-message picture x(64).

       77 NL picture x value x'0a'.

       linkage section.
       01 error-message picture x(64).
       01 need-abort picture 9.

       procedure division using error-message, need-abort.
       start-log-error.
           display NL error-message end-display
           call 'errnomessage' using
             by reference errno errno-name errno-message
           end-call
           display errno space errno-name errno-message end-display
           if need-abort is greater than zero
             stop run
           end-if.

       end program log-error.
