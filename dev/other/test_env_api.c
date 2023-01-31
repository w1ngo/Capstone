#include <stdio.h>
#include <stdlib.h>

int main(){

	// This works on exported variables only
	// 	Things like PATH and USERNAME that are already
	// 	exported will work automatically
	//
	// BLOCKSIZE, and other SHELL variables (vs global or environment
	// variables), need to be exported before being accessible
	// 	Unexported variables are interpreted simply as NULL
	const char *blocksizestr = getenv( "BLOCKSIZE" );
	printf("%s\n", blocksizestr);

	return 0;
}
