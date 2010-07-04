
%module panic
%{
	/* Includes the header in the wrapper code */
	#include "panic.h"
%}
 
/* Parse the header file to generate wrappers */
%include "panic.h"


