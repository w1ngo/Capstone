#include <stdio.h>
#include <string.h>

void process_args(int args, char* strings[]) {
    int i;

    printf("The program is called %s\n", strings[0]);

    for(i = 1; i < args; i++) {
        if     (strcmp(strings[i], "-name") == 0) { printf("name is %s\n", strings[ ++i ]); }
        else if(strcmp(strings[i], "-age" ) == 0) { printf("age is %2s\n", strings[ ++i ]); }
    else                                          { printf("argument %s not processed\n", strings[i]); }
    }
}

int main(int argc, char* argv[]) {
    int i;

    printf("%d arguments supplied\n", argc);
    for(i = 1; i < argc; ++i) { printf("%s\n", argv[i]); }

    process_args(argc, argv);
}
