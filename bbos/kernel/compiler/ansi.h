/* The <ansi.h> header attempts to decide whether the compiler has enough
 * conformance to Standard C for Minix to take advantage of.  If so, the
 * symbol _ANSI is defined (as 31415).  Otherwise _ANSI is not defined
 * here, but it may be defined by applications that want to bend the rules.
 * The magic number in the definition is to inhibit unnecessary bending
 * of the rules.  (For consistency with the new '#ifdef _ANSI" tests in
 * the headers, _ANSI should really be defined as nothing, but that would
 * break many library routines that use "#if _ANSI".)

 * If _ANSI ends up being defined, a macro
 *
 *	_PROTOTYPE(function, params)
 *
 * is defined.  This macro expands in different ways, generating either
 * ANSI Standard C prototypes or old-style K&R (Kernighan & Ritchie)
 * prototypes, as needed.  Finally, some programs use _CONST, _VOIDSTAR etc
 * in such a way that they are portable over both ANSI and K&R compilers.
 * The appropriate macros are defined here.
 */

#ifndef __BBOS_ANSI_H
#define __BBOS_ANSI_H

#define PROTOTYPE(proto, params) proto

#ifndef __BEGIN_DECLS
# ifdef  __cplusplus
#  define __BEGIN_DECLS  extern "C" {
#  define __END_DECLS    }
# else
#  define __BEGIN_DECLS
#  define __END_DECLS
# endif
#endif

#endif


