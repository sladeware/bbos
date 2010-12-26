/*
 * Copyright (c) 2011 Slade Maurer, Alexander Sviridenko
 */

#ifndef __UNSIGNED_MATH_H
#define __UNSIGNED_MATH_H

static int
umulf(int value, int fraction)
{
	int i, result, rest;
	
	result = rest = 0;
	
	for (i=1; i<17; i++)
	{
		if (fraction < 0) //b15 set
		{
			value >>= i;
			result += value;
			//result += (value >>> i); //accumulate integer result
			
			rest += ((value & ((1 << i) - 1)) << (16 - i)); //accumulate rest R/65536
			//if (CPU.carry()) result++; //update result if rest overflows
		}

		fraction <<= 1; //next bit
	}
	
	if (rest < 0) result++; //roundoff
printf("Result: %d\n",result);
	return result;
}

#endif



