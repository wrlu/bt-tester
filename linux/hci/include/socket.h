#ifndef HCI_SENDER_SOCKET
#define HCI_SENDER_SOCKET

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <sys/socket.h>
#include "../include/dev_mgmt.h"

#ifdef __cplusplus 
extern "C" {
#endif

int start();

#ifdef __cplusplus 
}
#endif

#endif