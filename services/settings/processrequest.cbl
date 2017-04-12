       identification division.
       program-id. process-request.

       data division.
       working-storage section.
       01 argc binary-long unsigned.
       01 need-more picture 9.

       linkage section.
       01 buffer.
         02 read-buffer.
           03 command picture x(11).
           03 args picture x(1013).
         02 buffer-length binary-long unsigned.
         02 data-length binary-long unsigned.
         02 write-buffer picture x(1024).
         02 output-length binary-long unsigned.
         02 sended binary-long unsigned.
         02 socket binary-int.

       procedure division using buffer.
         start-process-request.
      D     display data-length end-display
            if data-length is less than 11
              call 'addRead' using
                by value socket
              end-call
              goback
            end-if

            move data-length to argc
            subtract function length(command) from argc end-subtract
            subtract 1 from argc end-subtract

            call command using
              by reference argc
              by reference args
              by reference write-buffer
              by reference output-length
              returning need-more
              on exception
                move 'uc' to write-buffer
                move 2 to output-length
                move 0 to need-more
            end-call

            if need-more is greater than zero
              display 'need more argv' end-display
              call 'addRead' using
                by value socket
              end-call
              goback
            end-if

            move function length(read-buffer) to buffer-length
            move 1 to data-length

            move 1 to sended
            call 'addWrite' using
              by value socket
            end-call

            goback.
       end program process-request.
