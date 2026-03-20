#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <regex.h>

struct msg_buffer
{
    long msg_type;
    char msg_text[10000];
} message;

int main()
{
    key_t key=1234;
    int msgid=msgget(key,0666 | IPC_CREAT);

    msgrcv(msgid,&message,sizeof(message.msg_text),1,0);

    regex_t regex;
    int reti=regcomp(&regex,"<h1>.*</h1>",0);
    reti=regexec(&regex,message.msg_text,0,NULL,0);

    if(!reti)
    {
        printf("validare reusita\n");

        FILE *f=fopen("output.html","w");
        if(f==NULL)
        {
            perror("eroare la deschiderea fișierului");
            return 1;
        }
        fprintf(f,"%s",message.msg_text);
        fclose(f);

        printf("fisierul a fost salvat cu succes\n");
    }
    else
    {
        printf("validare esuata\n");
    }

    msgctl(msgid, IPC_RMID, NULL);
    regfree(&regex);
    return 0;
}
