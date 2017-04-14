       identification division.
       program-id. process-request.

       data division.
       working-storage section.
       01 argc binary-long unsigned.
       01 need-more picture 9.
       01 ind picture 9.

       01 commands-list.
         02 commands.
           03 filler picture x(11) value 'add-section'.
           03 filler picture x(11) value 'add-apikey '.
           03 filler picture x(11) value 'fix-section'.
           03 filler picture x(11) value 'get-section'.
         02 filler redefines commands.
           03 command-name picture x(11) occurs 4 times.


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

            move 'uc' to write-buffer
            move 2 to output-length
            move zero to need-more
            perform
              varying ind from 1 by 1 until ind is greater than 4
              if command-name(ind) is equal to command
                call command using
                  by reference argc
                  by reference args
                  by reference write-buffer
                  by reference output-length
                  returning need-more
                  on exception
                    move 'fl' to write-buffer
                    move 2 to output-length
                    move zero to need-more
                end-call
            end-perform

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
