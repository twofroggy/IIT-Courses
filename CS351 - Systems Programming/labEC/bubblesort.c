#include <stdio.h>
void swap (int *x, int *y)
{
	int t = *x;
	*x = *y;
	*y = t;
}

void bubblesort(int arr[], int num)
{
	int i, j;
	for (i = 0; i < num-1; i++) { 
		for (j = 0; j < num-i-1; j++) {
			if (arr[j] > arr[j+1]) {
				swap(&arr[j], &arr[j+1]);
			}
		}
	}
	int k = 0;
	for (k = 0; k < num; k++) {
		printf("%d ", arr[k]);
	}
	printf("\n");
}

int main(int argc, char **argv)
{
	//read in the second argument when calling this ftn, which would be pp2.txt
	FILE *fp = fopen("pp2.txt", "r"); 
	
	int a = 0;
	int size = 10;
	int arr[size];
	int b;
	
	fscanf(fp, "%d", &b);
	
	for (a = 0; a < size; a++) {
		printf("%d ", b);
		arr[a] = b;
		fscanf(fp, "%d", &b);
	}
	
	printf("\n");
	bubblesort(arr, size);
}

