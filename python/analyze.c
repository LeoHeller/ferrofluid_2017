#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

main()
{
  printf("Starting python3\n");
  // system("/usr/bin/python3 /home/pi/py/analyze_rpio.py");
  //execl("/bin/ls", "ls", "/home/pi/py", (char *) NULL);
  execl("/usr/bin/python3", "python3", "/home/pi/py/analyze_rpio.py", (char *) NULL);
}

