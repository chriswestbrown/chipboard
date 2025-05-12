#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

//pid_t getpid(void);

int main()
{
  pid_t pid = getpid();
  printf("foo with pid %d\n",pid);
  
  char buff[1024] = {'\0'};
  sprintf(buff,"hello%d.txt",pid);
  FILE* fout = fopen(buff,"w");
  fprintf(fout,"foo with pid %d\n",pid);
  fclose(fout);

  return 0;
}
