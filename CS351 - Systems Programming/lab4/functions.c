#include "functions.h"

double multiply(double a, double b)
{
	return a*b;
}

double divide(double a, double b)
{
	if(b == 0.0)
		return 0;
	else
		return a/b;
}

double add(double a, double b)
{
	return a+b;
}

double subtract(double a, double b)
{
	return a-b;
}
