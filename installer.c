#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

int main(int argc, char** argv)
{
    char buffer[32];
    setuid( 0 );
    if (argc == 1)
        system("./installer.py");
    else if (argc == 2)
    {
        snprintf(buffer, sizeof(buffer), "./installer.py %s", argv[1]);
        system(buffer);
    }
    else if (argc == 3)
    {
        snprintf(buffer, sizeof(buffer), "./installer.py %s %s", argv[1], argv[2]);
        system(buffer);
    }
    else
    {
        printf("Program accepts no more than 3 arguments. \n");
        printf("Example ./runscript <config_name> -verbose. \n");
    }

    return 0;
}
