#include "../include/socket.h"

int send_hci_dev_info_list(int sk) {
    int dev_id_list[HCI_MAX_DEV];
    size_t dev_num;
    int i, ret = -1, err = 0;

    ret = get_hci_dev_list(dev_id_list, HCI_MAX_DEV, &dev_num);
    
    if (ret) 
        printf("[socket] send_hci_dev_info_list: get_hci_dev_list returns error code %d.\n", ret);

    struct hci_dev_info **dev_info_list = (struct hci_dev_info **) calloc(dev_num, sizeof(struct hci_dev_info *));
    if (!dev_info_list) {
        free(dev_info_list);
		err = -errno;
		return err;
	}

    for (i = 0; i < dev_num; ++i) {
        dev_info_list[i] = (struct hci_dev_info *) malloc(sizeof(struct hci_dev_info));
        if (!dev_info_list[i]) {
            free(dev_info_list[i]);
		    err = -errno;
		    break;
	    }
        memset(dev_info_list[i], 0, sizeof(struct hci_dev_info));

        ret = get_hci_dev_info(dev_id_list[i], dev_info_list[i]);

        if (ret)
            printf("[socket] send_hci_dev_info_list: get_hci_dev_info for dev_id %d returns error code %d.\n", i, ret);
        char info_str[100];
        get_hci_dev_info_str(info_str, 100, dev_info_list[i]);
        printf("%s", info_str);
        free(dev_info_list[i]);
    }

    free(dev_info_list);
    return err;
}

int on_receive() {

}

int start() {
    send_hci_dev_info_list(-1);
    return 0;
}