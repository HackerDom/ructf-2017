       identification division.
       program-id. errnomessage.
      *
      *  Copyright (C) 2014 Steve Williams <stevewilliams38@gmail.com>
      *
      *  This program is free software; you can redistribute it and/or
      *  modify it under the terms of the GNU General Public License as
      *  published by the Free Software Foundation; either version 2,
      *  or (at your option) any later version.
      *
      *  This program is distributed in the hope that it will be useful,
      *  but WITHOUT ANY WARRANTY; without even the implied warranty of
      *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
      *  GNU General Public License for more details.
      *
      *  You should have received a copy of the GNU General Public
      *  License along with this software; see the file COPYING.
      *  If not, write to the Free Software Foundation, Inc.,
      *  59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

      * ============================================================
      * Get the current errno and return the errno, errno name
      * and errno message.
      *
      * The call to the c subroutine get_errno may be replaced by
      * a GNU COBOL function call in the future.
      * ============================================================


       data division.
       linkage section.
       01  errno binary-char unsigned.
       01  errno-name picture x(16).
       01  errno-message picture x(64).
       procedure division using errno, errno-name, errno-message.
       start-errno-message.
           call 'get_errno' returning errno end-call
           evaluate errno
           when 0
               move 'OK' to errno-name
               move spaces to errno-message
           when 1
               move 'EPERM' to errno-name
               move 'Operation not permitted' to errno-message
           when 2
               move 'ENOENT' to errno-name
               move 'No such file or directory' to errno-message
           when 3
               move 'ESRCH' to errno-name
               move 'No such process' to errno-message
           when 4
               move 'EINTR' to errno-name
               move 'Interrupted system call' to errno-message
           when 5
               move 'EIO' to errno-name
               move 'I/O error' to errno-message
           when 6
               move 'ENXIO' to errno-name
               move 'No such device or address' to errno-message
           when 7
               move 'E2BIG' to errno-name
               move 'Argument list too long' to errno-message
           when 8
               move 'ENOEXEC' to errno-name
               move 'Exec format error' to errno-message
           when 9
               move 'EBADF' to errno-name
               move 'Bad file number' to errno-message
           when 10
               move 'ECHILD' to errno-name
               move 'No child processes' to errno-message
           when 11
               move 'EAGAIN' to errno-name
               move 'Try again' to errno-message
           when 12
               move 'ENOMEM' to errno-name
               move 'Out of memory' to errno-message
           when 13
               move 'EACCES' to errno-name
               move 'Permission denied' to errno-message
           when 14
               move 'EFAULT' to errno-name
               move 'Bad address' to errno-message
           when 15
               move 'ENOTBLK' to errno-name
               move 'Block device required' to errno-message
           when 16
               move 'EBUSY' to errno-name
               move 'Device or resource busy' to errno-message
           when 17
               move 'EEXIST' to errno-name
               move 'File exists' to errno-message
           when 18
               move 'EXDEV' to errno-name
               move 'Cross-device link' to errno-message
           when 19
               move 'ENODEV' to errno-name
               move 'No such device' to errno-message
           when 20
               move 'ENOTDIR' to errno-name
               move 'Not a directory' to errno-message
           when 21
               move 'EISDIR' to errno-name
               move 'Is a directory' to errno-message
           when 22
               move 'EINVAL' to errno-name
               move 'Invalid argument' to errno-message
           when 23
               move 'ENFILE' to errno-name
               move 'File table overflow' to errno-message
           when 24
               move 'EMFILE' to errno-name
               move 'Too many open files' to errno-message
           when 25
               move 'ENOTTY' to errno-name
               move 'Not a typewriter' to errno-message
           when 26
               move 'ETXTBSY' to errno-name
               move 'Text file busy' to errno-message
           when 27
               move 'EFBIG' to errno-name
               move 'File too large' to errno-message
           when 28
               move 'ENOSPC' to errno-name
               move 'No space left on device' to errno-message
           when 29
               move 'ESPIPE' to errno-name
               move 'Illegal seek' to errno-message
           when 30
               move 'EROFS' to errno-name
               move 'Read-only file system' to errno-message
           when 31
               move 'EMLINK' to errno-name
               move 'Too many links' to errno-message
           when 32
               move 'EPIPE' to errno-name
               move 'Broken pipe' to errno-message
           when 33
               move 'EDOM' to errno-name
               move 'Math argument out of domain of func'
                   to errno-message
           when 34
               move 'ERANGE' to errno-name
               move 'Math result not representable' to errno-message
           when 35
               move 'EDEADLK' to errno-name
               move 'Resource deadlock would occur' to errno-message
           when 36
               move 'ENAMETOOLONG' to errno-name
               move 'File name too long' to errno-message
           when 37
               move 'ENOLCK' to errno-name
               move 'No record locks available' to errno-message
           when 38
               move 'ENOSYS' to errno-name
               move 'Function not implemented' to errno-message
           when 39
               move 'ENOTEMPTY' to errno-name
               move 'Directory not empty' to errno-message
           when 40
               move 'ELOOP' to errno-name
               move 'Too many symbolic links encountered'
                   to errno-message
           when 41
               move 'EWOULDBLOCK' to errno-name
               move 'Operation would block' to errno-message
           when 42
               move 'ENOMSG' to errno-name
               move 'No message of desired type' to errno-message
           when 43
               move 'EIDRM' to errno-name
               move 'Identifier removed' to errno-message
           when 44
               move 'ECHRNG' to errno-name
               move 'Channel number out of range' to errno-message
           when 45
               move 'EL2NSYNC' to errno-name
               move 'Level 2 not synchronized' to errno-message
           when 46
               move 'EL3HLT' to errno-name
               move 'Level 3 halted' to errno-message
           when 47
               move 'EL3RST' to errno-name
               move 'Level 3 reset' to errno-message
           when 48
               move 'ELNRNG' to errno-name
               move 'Link number out of range' to errno-message
           when 49
               move 'EUNATCH' to errno-name
               move 'Protocol driver not attached' to errno-message
           when 50
               move 'ENOCSI' to errno-name
               move 'No CSI structure available' to errno-message
           when 51
               move 'EL2HLT' to errno-name
               move 'Level 2 halted' to errno-message
           when 52
               move 'EBADE' to errno-name
               move 'Invalid exchange' to errno-message
           when 53
               move 'EBADR' to errno-name
               move 'Invalid request descriptor' to errno-message
           when 54
               move 'EXFULL' to errno-name
               move 'Exchange full' to errno-message
           when 55
               move 'ENOANO' to errno-name
               move 'No anode' to errno-message
           when 56
               move 'EBADRQC' to errno-name
               move 'Invalid request code' to errno-message
           when 57
               move 'EBADSLT' to errno-name
               move 'Invalid slot' to errno-message
           when 58
               move 'EDEADLOCK' to errno-name
               move 'deadlock' to errno-message
           when 59
               move 'EBFONT' to errno-name
               move 'Bad font file format' to errno-message
           when 60
               move 'ENOSTR' to errno-name
               move 'Device not a stream' to errno-message
           when 61
               move 'ENODATA' to errno-name
               move 'No data available' to errno-message
           when 62
               move 'ETIME' to errno-name
               move 'Timer expired' to errno-message
           when 63
               move 'ENOSR' to errno-name
               move 'Out of streams resources' to errno-message
           when 64
               move 'ENONET' to errno-name
               move 'Machine is not on the network' to errno-message
           when 65
               move 'ENOPKG' to errno-name
               move 'Package not installed' to errno-message
           when 66
               move 'EREMOTE' to errno-name
               move 'Object is remote' to errno-message
           when 67
               move 'ENOLINK' to errno-name
               move 'Link has been severed' to errno-message
           when 68
               move 'EADV' to errno-name
               move 'Advertise error' to errno-message
           when 69
               move 'ESRMNT' to errno-name
               move 'Srmount error' to errno-message
           when 70
               move 'ECOMM' to errno-name
               move 'Communication error on send' to errno-message
           when 71
               move 'EPROTO' to errno-name
               move 'Protocol error' to errno-message
           when 72
               move 'EMULTIHOP' to errno-name
               move 'Multihop attempted' to errno-message
           when 73
               move 'EDOTDOT' to errno-name
               move 'RFS specific error' to errno-message
           when 74
               move 'EBADMSG' to errno-name
               move 'Not a data message' to errno-message
           when 75
               move 'EOVERFLOW' to errno-name
               move 'Value too large for defined data type'
                   to errno-message
           when 76
               move 'ENOTUNIQ' to errno-name
               move 'Name not unique on network' to errno-message
           when 77
               move 'EBADFD' to errno-name
               move 'File descriptor in bad state' to errno-message
           when 78
               move 'EREMCHG' to errno-name
               move 'Remote address changed' to errno-message
           when 79
               move 'ELIBACC' to errno-name
               move 'Can not access a needed shared library'
                    to errno-message
           when 80
               move 'ELIBBAD' to errno-name
               move 'Accessing a corrupted shared library'
                   to errno-message
           when 81
               move 'ELIBSCN' to errno-name
               move '.lib section in a.out corrupted' to errno-message
           when 82
               move 'ELIBMAX' to errno-name
               move 'Attempting to link in too many shared libraries'
                    to errno-message
           when 83
               move 'ELIBEXEC' to errno-name
               move 'Cannot exec a shared library directly'
                   to errno-message
           when 84
               move 'EILSEQ' to errno-name
               move 'Illegal byte sequence' to errno-message
           when 85
               move 'ERESTART' to errno-name
               move 'Interrupted system call should be restarted'
                   to errno-message
           when 86
               move 'ESTRPIPE' to errno-name
               move 'Streams pipe error' to errno-message
           when 87
               move 'EUSERS' to errno-name
               move 'Too many users' to errno-message
           when 88
               move 'ENOTSOCK' to errno-name
               move 'Socket operation on non-socket' to errno-message
           when 89
               move 'EDESTADDRREQ' to errno-name
               move 'Destination address required' to errno-message
           when 90
               move 'EMSGSIZE' to errno-name
               move 'Message too long' to errno-message
           when 91
               move 'EPROTOTYPE' to errno-name
               move 'Protocol wrong type for socket' to errno-message
           when 92
               move 'ENOPROTOOPT' to errno-name
               move 'Protocol not available' to errno-message
           when 93
               move 'EPROTONOSUPPORT' to errno-name
               move 'Protocol not supported' to errno-message
           when 94
               move 'ESOCKTNOSUPPORT' to errno-name
               move 'Socket type not supported' to errno-message
           when 95
               move 'EOPNOTSUPP' to errno-name
               move 'Operation not supported on transport endpoint'
                   to errno-message
           when 96
               move 'EPFNOSUPPORT' to errno-name
               move 'Protocol family not supported' to errno-message
           when 97
               move 'EAFNOSUPPORT' to errno-name
               move 'Address family not supported by protocol'
                   to errno-message
           when 98
               move 'EADDRINUSE' to errno-name
               move 'Address already in use' to errno-message
           when 99
               move 'EADDRNOTAVAIL' to errno-name
               move 'Cannot assign requested address' to errno-message
           when 100
               move 'ENETDOWN' to errno-name
               move 'Network is down' to errno-message
           when 101
               move 'ENETUNREACH' to errno-name
               move 'Network is unreachable' to errno-message
           when 102
               move 'ENETRESET' to errno-name
               move 'Network dropped connection because of reset'
                   to errno-message
           when 103
               move 'ECONNABORTED' to errno-name
               move 'Software caused connection abort' to errno-message
           when 104
               move 'ECONNRESET' to errno-name
               move 'Connection reset by peer' to errno-message
           when 105
               move 'ENOBUFS' to errno-name
               move 'No buffer space available' to errno-message
           when 106
               move 'EISCONN' to errno-name
               move 'Transport endpoint is already connected'
                    to errno-message
           when 107
               move 'ENOTCONN' to errno-name
               move 'Transport endpoint is not connected'
                   to errno-message
           when 108
               move 'ESHUTDOWN' to errno-name
               move 'Cannot send after transport endpoint shutdown'
                   to errno-message
           when 109
               move 'ETOOMANYREFS' to errno-name
               move 'Too many references: cannot splice'
                   to errno-message
           when 110
               move 'ETIMEDOUT' to errno-name
               move 'Connection timed out' to errno-message
           when 111
               move 'ECONNREFUSED' to errno-name
               move 'Connection refused' to errno-message
           when 112
               move 'EHOSTDOWN' to errno-name
               move 'Host is down' to errno-message
           when 113
               move 'EHOSTUNREACH' to errno-name
               move 'No route to host' to errno-message
           when 114
               move 'EALREADY' to errno-name
               move 'Operation already in progress' to errno-message
           when 115
               move 'EINPROGRESS' to errno-name
               move 'Operation now in progress' to errno-message
           when 116
               move 'ESTALE' to errno-name
               move 'Stale NFS file handle' to errno-message
           when 117
               move 'EUCLEAN' to errno-name
               move 'Structure needs cleaning' to errno-message
           when 118
               move 'ENOTNAM' to errno-name
               move 'Not a XENIX named type file' to errno-message
           when 119
               move 'ENAVAIL' to errno-name
               move 'No XENIX semaphores available' to errno-message
           when 120
               move 'EISNAM' to errno-name
               move 'Is a named type file' to errno-message
           when 121
               move 'EREMOTEIO' to errno-name
               move 'Remote I/O error' to errno-message
           when 122
               move 'EDQUOT' to errno-name
               move 'Quota exceeded' to errno-message
           when 123
               move 'ENOMEDIUM' to errno-name
               move 'No medium found' to errno-message
           when 124
               move 'EMEDIUMTYPE' to errno-name
               move 'Wrong medium type' to errno-message
           when 125
               move 'ECANCELED' to errno-name
               move 'Operation Canceled' to errno-message
           when 126
               move 'ENOKEY' to errno-name
               move 'Required key not available' to errno-message
           when 127
               move 'EKEYEXPIRED' to errno-name
               move 'Key has expired' to errno-message
           when 128
               move 'EKEYREVOKED' to errno-name
               move 'Key has been revoked' to errno-message
           when 129
               move 'EKEYREJECTED' to errno-name
               move 'Key was rejected by service' to errno-message
           when 130
               move 'EOWNERDEAD' to errno-name
               move 'Owner died' to errno-message
           when 131
               move 'ENOTRECOVERABLE' to errno-name
               move 'State not recoverable' to errno-message
           when 132
               move 'ERFKILL' to errno-name
               move 'Operation not possible due to RF-kill'
                   to errno-message
           when 133
               move 'EHWPOISON' to errno-name
               move 'Memory page has hardware error' to errno-message
           when other
               move 'UNKNOWN' to errno-name
               move 'Unknown errorno' to errno-message
           end-evaluate
           goback.
       end program errnomessage.
