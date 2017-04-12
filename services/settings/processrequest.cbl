       identification division.
       program-id. process-request.

       data division.
       linkage section.
       01 buffer.
         02 read-buffer.
           03 command picture x(10).
           03 args picture x(1014).
         02 buffer-length binary-long unsigned.
         02 data-length binary-long unsigned.
         02 write-buffer picture x(1024).
         02 output-length binary-long unsigned.
         02 sended binary-long unsigned.
         02 socket binary-int.

       procedure division using buffer.
         start-process-request.
      D     display data-length end-display
            if data-length is less than 10
              call 'addRead' using
                by value socket
              end-call
              goback
            end-if
            move read-buffer to write-buffer
            move data-length to output-length
            subtract 1 from output-length
            move 1 to sended
            move function length(read-buffer) to buffer-length
            move 1 to data-length
            call 'addWrite' using
              by value socket
            end-call

            goback.
       end program process-request.
