#ifndef HCI_SENDER_DEV_MGMT
#define HCI_SENDER_DEV_MGMT

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <sys/socket.h>
#include <sys/ioctl.h>
#include <bluetooth/bluetooth.h>
#include <bluetooth/hci.h>
#include <bluetooth/hci_lib.h>

#ifdef __cplusplus 
extern "C" {
#endif

struct hci_dev_info;

int get_hci_dev_list(int dev_id_list[], size_t len, size_t *dev_num);
int get_first_hci_dev();
int get_hci_dev_info(int dev_id, struct hci_dev_info *di);
void get_hci_dev_info_str(char *str, size_t size, struct hci_dev_info *info);

#ifdef __cplusplus 
}
#endif

#endif