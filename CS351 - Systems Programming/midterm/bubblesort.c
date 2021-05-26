#include <stdio.h>
void bubblesort(int arr[], int n){
	int i,j;
	for (i=0;i<n-1;i++) {
		for (j=0;j<n-i-1;i++) {
			if (arr[j] > arr[j+1]) {
				swap(&arr[j], &arr[j+1]);
			}
		}
	}
}

void swap(int *ptr, int *sptr) {
	int buf = *ptr;
	*ptr = *sptr;
	*sptr = buf;
}


int main()
{
 	int arr[] = fgets(stdin);
	int n = sizeof(arr)/sizeof(arr[0]);
	bubblesort(arr, n);
	printf("Sorted array: \n");
	printArray(arr, n);

	return 0;
}

