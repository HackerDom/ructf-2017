/* MHD_config.h.  Generated from MHD_config.h.in by configure.  */
/* MHD_config.h.in.  Generated from configure.ac by autoheader.  */

#define _GNU_SOURCE  1

/* Define if building universal (internal helper macro) */
/* #undef AC_APPLE_UNIVERSAL_BUILD */

/* This is a Cygwin system */
/* #undef CYGWIN */

/* disable basic and digest Auth support */
#define DAUTH_SUPPORT 1

/* This is a FreeBSD system */
/* #undef FREEBSD */

/* Define to 1 if you have the <arpa/inet.h> header file. */
#define HAVE_ARPA_INET_H 1

/* Define to 1 if you have the declaration of `TCP_CORK', and to 0 if you
   don't. */
#define HAVE_DECL_TCP_CORK 1

/* Define to 1 if you have the declaration of `TCP_NOPUSH', and to 0 if you
   don't. */
#define HAVE_DECL_TCP_NOPUSH 0

/* Define to 1 if you have the <dlfcn.h> header file. */
#define HAVE_DLFCN_H 1

/* Define to 1 if you have the <errno.h> header file. */
#define HAVE_ERRNO_H 1

/* Define to 1 if you have the <fcntl.h> header file. */
#define HAVE_FCNTL_H 1

/* Define to 1 if fseeko (and presumably ftello) exists and is declared. */
#define HAVE_FSEEKO 1

/* We have gnutls */
#define HAVE_GNUTLS 0

/* Define to 1 if you have the <gnutls/gnutls.h> header file. */
/* #undef HAVE_GNUTLS_GNUTLS_H */

/* Provides IPv6 headers */
#define HAVE_INET6 1

/* Define to 1 if you have the <inttypes.h> header file. */
#define HAVE_INTTYPES_H 1

/* Define to 1 if you have a functional curl library. */
/* #undef HAVE_LIBCURL */

/* Define to 1 if you have the <limits.h> header file. */
#define HAVE_LIMITS_H 1

/* can use shutdown on listen sockets */
#define HAVE_LISTEN_SHUTDOWN 1

/* Define to 1 if you have the <locale.h> header file. */
#define HAVE_LOCALE_H 1

/* Define to 1 if you have the <math.h> header file. */
#define HAVE_MATH_H 1

/* Define to 1 if you have the `memmem' function. */
#define HAVE_MEMMEM 1

/* Define to 1 if you have the <memory.h> header file. */
#define HAVE_MEMORY_H 1

/* Disable error messages */
#define HAVE_MESSAGES 1

/* Define to 1 if you have the <netdb.h> header file. */
#define HAVE_NETDB_H 1

/* Define to 1 if you have the <netinet/in.h> header file. */
#define HAVE_NETINET_IN_H 1

/* Define to 1 if you have the <netinet/tcp.h> header file. */
#define HAVE_NETINET_TCP_H 1

/* Define to 1 if you have the <plibc.h> header file. */
/* #undef HAVE_PLIBC_H */

/* Define to 1 if you have the <poll.h> header file. */
#define HAVE_POLL_H 1

/* Define to 1 if you have the <pthread.h> header file. */
#define HAVE_PTHREAD_H 1

/* Define to 1 if you have the <stdint.h> header file. */
#define HAVE_STDINT_H 1

/* Define to 1 if you have the <stdio.h> header file. */
#define HAVE_STDIO_H 1

/* Define to 1 if you have the <stdlib.h> header file. */
#define HAVE_STDLIB_H 1

/* Define to 1 if you have the <strings.h> header file. */
#define HAVE_STRINGS_H 1

/* Define to 1 if you have the <string.h> header file. */
#define HAVE_STRING_H 1

/* Define to 1 if you have the <sys/mman.h> header file. */
#define HAVE_SYS_MMAN_H 1

/* Define to 1 if you have the <sys/msg.h> header file. */
#define HAVE_SYS_MSG_H 1

/* Define to 1 if you have the <sys/select.h> header file. */
#define HAVE_SYS_SELECT_H 1

/* Define to 1 if you have the <sys/socket.h> header file. */
#define HAVE_SYS_SOCKET_H 1

/* Define to 1 if you have the <sys/stat.h> header file. */
#define HAVE_SYS_STAT_H 1

/* Define to 1 if you have the <sys/time.h> header file. */
#define HAVE_SYS_TIME_H 1

/* Define to 1 if you have the <sys/types.h> header file. */
#define HAVE_SYS_TYPES_H 1

/* Define to 1 if you have the <time.h> header file. */
#define HAVE_TIME_H 1

/* Define to 1 if you have the <unistd.h> header file. */
#define HAVE_UNISTD_H 1

/* Define to 1 if you have the <winsock2.h> header file. */
/* #undef HAVE_WINSOCK2_H */

/* Define to 1 if you have the <ws2tcpip.h> header file. */
/* #undef HAVE_WS2TCPIP_H */

/* disable HTTPS support */
#define HTTPS_SUPPORT 0

/* Defined if libcurl supports AsynchDNS */
/* #undef LIBCURL_FEATURE_ASYNCHDNS */

/* Defined if libcurl supports IDN */
/* #undef LIBCURL_FEATURE_IDN */

/* Defined if libcurl supports IPv6 */
/* #undef LIBCURL_FEATURE_IPV6 */

/* Defined if libcurl supports KRB4 */
/* #undef LIBCURL_FEATURE_KRB4 */

/* Defined if libcurl supports libz */
/* #undef LIBCURL_FEATURE_LIBZ */

/* Defined if libcurl supports NTLM */
/* #undef LIBCURL_FEATURE_NTLM */

/* Defined if libcurl supports SSL */
/* #undef LIBCURL_FEATURE_SSL */

/* Defined if libcurl supports SSPI */
/* #undef LIBCURL_FEATURE_SSPI */

/* Defined if libcurl supports DICT */
/* #undef LIBCURL_PROTOCOL_DICT */

/* Defined if libcurl supports FILE */
/* #undef LIBCURL_PROTOCOL_FILE */

/* Defined if libcurl supports FTP */
/* #undef LIBCURL_PROTOCOL_FTP */

/* Defined if libcurl supports FTPS */
/* #undef LIBCURL_PROTOCOL_FTPS */

/* Defined if libcurl supports HTTP */
/* #undef LIBCURL_PROTOCOL_HTTP */

/* Defined if libcurl supports HTTPS */
/* #undef LIBCURL_PROTOCOL_HTTPS */

/* Defined if libcurl supports LDAP */
/* #undef LIBCURL_PROTOCOL_LDAP */

/* Defined if libcurl supports TELNET */
/* #undef LIBCURL_PROTOCOL_TELNET */

/* Defined if libcurl supports TFTP */
/* #undef LIBCURL_PROTOCOL_TFTP */

/* This is a Linux system */
#define LINUX 1

/* Define to the sub-directory in which libtool stores uninstalled libraries.
   */
#define LT_OBJDIR ".libs/"

/* gcrypt lib version */
#define MHD_GCRYPT_VERSION "1:1.2.2"

/* gnuTLS lib version - used in conjunction with cURL */
#define MHD_REQ_CURL_GNUTLS_VERSION "2.8.6"

/* NSS lib version - used in conjunction with cURL */
#define MHD_REQ_CURL_NSS_VERSION "3.12.0"

/* required cURL SSL version to run tests */
#define MHD_REQ_CURL_OPENSSL_VERSION "0.9.8"

/* required cURL version to run tests */
#define MHD_REQ_CURL_VERSION "7.16.4"

/* This is a MinGW system */
/* #undef MINGW */

/* This is a NetBSD system */
/* #undef NETBSD */

/* Define to 1 if your C compiler doesn't accept -c and -o together. */
/* #undef NO_MINUS_C_MINUS_O */

/* This is an OpenBSD system */
/* #undef OPENBSD */

/* This is a OS/390 system */
/* #undef OS390 */

/* This is an OS X system */
/* #undef OSX */

/* Some strange OS */
/* #undef OTHEROS */

/* Name of package */
#define PACKAGE "libmicrohttpd"

/* Define to the address where bug reports for this package should be sent. */
#define PACKAGE_BUGREPORT "libmicrohttpd@gnu.org"

/* Define to the full name of this package. */
#define PACKAGE_NAME "libmicrohttpd"

/* Define to the full name and version of this package. */
#define PACKAGE_STRING "libmicrohttpd 0.9.16"

/* Define to the one symbol short name of this package. */
#define PACKAGE_TARNAME "libmicrohttpd"

/* Define to the home page for this package. */
#define PACKAGE_URL ""

/* Define to the version of this package. */
#define PACKAGE_VERSION "0.9.16"

/* This is a Solaris system */
/* #undef SOLARIS */

/* This is a BSD system */
/* #undef SOMEBSD */

/* Define to 1 if you have the ANSI C header files. */
#define STDC_HEADERS 1

/* Version number of package */
#define VERSION "0.9.16"

/* This is a Windows system */
/* #undef WINDOWS */

/* Define WORDS_BIGENDIAN to 1 if your processor stores words with the most
   significant byte first (like Motorola and SPARC, unlike Intel). */
#if defined AC_APPLE_UNIVERSAL_BUILD
# if defined __BIG_ENDIAN__
#  define WORDS_BIGENDIAN 1
# endif
#else
# ifndef WORDS_BIGENDIAN
/* #  undef WORDS_BIGENDIAN */
# endif
#endif

/* Number of bits in a file offset, on hosts where this is settable. */
/* #undef _FILE_OFFSET_BITS */

/* Define to 1 to make fseeko visible on some hosts (e.g. glibc 2.2). */
/* #undef _LARGEFILE_SOURCE */

/* Define for large files, on AIX-style hosts. */
/* #undef _LARGE_FILES */

/* Need with solaris or errno doesnt work */
/* #undef _REENTRANT */

/* Define curl_free() as free() if our version of curl lacks curl_free. */
/* #undef curl_free */
