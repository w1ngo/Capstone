#include <stdio.h>

int add( int a, int b, int c ) {
	return a + b + c;
}

int greater( int a, int b ) {
	return ((a >= b) * a) + ((a < b) * b);
}
