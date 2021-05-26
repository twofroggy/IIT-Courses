#include <stdio.h>
#include <string.h>
void hash(char *s)
{
	int n = (int)(strlen(s));
	int sum = 0; 
	int i;
	for (i = 0; i < n; i++)
	{
		sum += (int)(s[i]);
	}
	printf("OUTPUT: %d\n", sum);
} 
 
int main(int argc, char *argv[])
{
	hash(argv[1]);
	return 0;
}

