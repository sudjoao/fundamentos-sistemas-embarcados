#include <stdio.h>
#include <unistd.h>         //Used for UART
#include <fcntl.h>          //Used for UART
#include <termios.h>        //Used for UART
#include <string.h>      

char getOptionValue(int option){
    if(option == 1){
        return 0xA1;
    }else if(option == 2){
        return 0xA2;
    }else if(option == 3){
        return 0xA3;
    }else if(option == 4){
        return 0xB1;
    }else if(option == 5){
        return 0xB2;
    }else {
        return 0xB3;
    }
}

void printOutput(int option, unsigned char* buffer, int size){
    if(option == 1){
        int data;
        memcpy(&data, buffer, size);
        printf("O número recebido foi: %d\n", data);
    }else if(option == 2){
        float data;
        memcpy(&data, buffer, size);
        printf("O número recebido foi: %f\n", data);
    }else if(option == 3){
        char data[255];
        memcpy(&data, buffer, size);
        data[size] = '\0';
        printf("O texto recebido foi: %s\n", data);
    }

}

int main(int argc, const char * argv[]) {

    int uart0_filestream = -1;
    int option;
    scanf("%d", &option);
    char optionValue = getOptionValue(option);
    int isReadOp = option > 3 ? 0 : 1;

    uart0_filestream = open("/dev/serial0", O_RDWR | O_NOCTTY | O_NDELAY);      //Open in non blocking read/write mode
    if (uart0_filestream == -1)
    {
        printf("Erro - Não foi possível iniciar a UART.\n");
    }
    else
    {
        printf("UART inicializada!\n");
    }    
    struct termios options;
    tcgetattr(uart0_filestream, &options);
    options.c_cflag = B9600 | CS8 | CLOCAL | CREAD;     //<Set baud rate
    options.c_iflag = IGNPAR;
    options.c_oflag = 0;
    options.c_lflag = 0;
    tcflush(uart0_filestream, TCIFLUSH);
    tcsetattr(uart0_filestream, TCSANOW, &options);

    unsigned char tx_buffer[20];
    unsigned char *p_tx_buffer;
    
    p_tx_buffer = &tx_buffer[0];
    *p_tx_buffer++ = optionValue;
    *p_tx_buffer++ = 3;
    *p_tx_buffer++ = 9;
    *p_tx_buffer++ = 1;
    *p_tx_buffer++ = 0;

    printf("Buffers de memória criados!\n");
    
    if (uart0_filestream != -1)
    {
        printf("Escrevendo caracteres na UART ...");
        int count = write(uart0_filestream, &tx_buffer[0], (p_tx_buffer - &tx_buffer[0]));
        if (count < 0)
        {
            printf("UART TX error\n");
        }
        else
        {
            printf("escrito.\n");
        }
    }

    sleep(1);

    //----- CHECK FOR ANY RX BYTES -----
    if (uart0_filestream != -1)
    {
        // Read up to 255 characters from the port if they are there
        unsigned char rx_buffer[256];
        int data;
        int rx_length = read(uart0_filestream, (void*)rx_buffer, 255);      //Filestream, buffer to store in, number of bytes to read (max)
        if (rx_length < 0)
        {
            printf("Erro na leitura.\n"); //An error occured (will occur if there are no bytes)
        }
        else if (rx_length == 0)
        {
            printf("Nenhum dado disponível.\n"); //No data waiting
        }
        else
        {
            //Bytes received
            printf("%i Bytes lidos\n");
            printOutput(option, rx_buffer, rx_length);
        }
    }

    close(uart0_filestream);
   return 0;
}
