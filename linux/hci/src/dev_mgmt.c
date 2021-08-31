#include "../include/dev_mgmt.h"

int get_hci_dev_list(int dev_id_list[], size_t len, size_t *dev_num) {
    struct hci_dev_list_req *dl;
	struct hci_dev_req *dr;

    int i, sk, err = 0;

    sk = socket(AF_BLUETOOTH, SOCK_RAW | SOCK_CLOEXEC, BTPROTO_HCI);
	if (sk < 0)
		return sk;

    dl = malloc(HCI_MAX_DEV * sizeof(*dr) + sizeof(*dl));
	if (!dl) {
        free(dl);
		err = -errno;
		return err;
	}
    
    memset(dl, 0, HCI_MAX_DEV * sizeof(*dr) + sizeof(*dl));

    dl->dev_num = HCI_MAX_DEV;
    dr = dl->dev_req;

    if (ioctl(sk, HCIGETDEVLIST, (void *) dl) < 0) {
        free(dl);
		err = -errno;
		return err;
	}

    *dev_num = dl->dev_num;

    if (len >= dl->dev_num) {
        len = dl->dev_num;
    } else {
        printf("[dev_mgmt] get_hci_dev_list: dev_id buffer too small, %d < %d.\n", len, dl->dev_num);
    }

    for (i = 0; i < len; i++, dr++) {
        if (i < len) {
            dev_id_list[i] = dr->dev_id;
        }
	}

    free(dl);
    close(sk);
	errno = err;

    return err;
}

int get_first_hci_dev() {
    return hci_get_route(NULL);
}

int get_hci_dev_info(int dev_id, struct hci_dev_info *di) {
    return hci_devinfo(dev_id, di);
}

int open_hci_dev_socket(int dev_id) {
    return hci_open_dev(dev_id);
}

void get_hci_dev_info_str(char *str, size_t size, struct hci_dev_info *info) {
    if (str == NULL || size == 0) {
        return;
    }
    char bdaddr_str[18];
    ba2str(&info->bdaddr, bdaddr_str);
    snprintf(str, size, "{dev_id: %d, name: '%s', bdaddr: '%s', flags: '%s', type: '%s'}\n",
        info->dev_id, info->name, bdaddr_str, 
        hci_dflagstostr(info->flags), hci_bustostr(info->type));
}
