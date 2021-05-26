#include <stdio.h>
int hash (char *s) {
	int total = 0; 
        char[] c; 
        c = s.ToCharArray(); 
	for (int k = 0; k <= c.GetUpperBound(0); k++) {
		total += (int)c[k]; 
	}
	return total % array.GetUpperBound(0); 

int main()
{
	return 0;
}

