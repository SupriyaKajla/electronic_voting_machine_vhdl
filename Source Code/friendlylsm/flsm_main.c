#include <linux/lsm_hooks.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/proc_fs.h>
#include <asm/uaccess.h>
#include <linux/module.h>
#include <linux/seq_file.h>
#include <linux/fs.h>
#include <asm/segment.h>
#include <linux/buffer_head.h>
#include <linux/uaccess.h>
#include <linux/init.h>
#include <linux/watchdog.h>
#include <linux/delay.h>
#include <linux/syscalls.h>
#include <linux/fcntl.h>
#include <linux/file.h>
#include <linux/slab.h>
#include <linux/moduleparam.h>
#include <linux/stat.h>
#include <linux/printk.h>
#include <linux/miscdevice.h>
#include <linux/sched.h>
#include <linux/string.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("NF, SK");
MODULE_DESCRIPTION("Friendly LSM - Filehook with GUI");
MODULE_VERSION("0.01");

#define MY_FILE "/home/flsm/Desktop/flsm.txt"
char buf[128];
struct file *file = NULL;
void *in_buf;
const void *out_buf;




//Start Hard Data from GUI
int count = 5; //count

const char * proglist[] = {"node","gnome-calculato","gedit","gnome-screenshot","other"}; //proglist
const char * proglistdprfiles[] = {"S","W","W","S","A"}; //progsettingslist

const char * w_settings[] = {"1","1","0"}; //wsettingslist
const char * s_settings[] = {"1","1","1"}; //ssettingslist
const char * a_settings[] = {"1","1","0"}; //asettingslist

int s_allow_userscount = 2;
const char * s_allow_users[] = { "1", "0" };

int s_rest_userscount = 1;
const char * s_rest_users[] = { "1000"};

int w_allow_userscount = 2;
const char * w_allow_users[] = { "1", "0" };

int w_restric_userscount = 1;
const char * w_restric_users[] = { "1000"};




//settings index 0 - audit, 1- give warning , 2- restrict-access,

//A -- Audit --  only Audit
//W -- Warning -- only audit and log complain
//S -- Strict -- Stop execution, audit

//End Hard Data from GUI




static struct miscdevice my_module_cnf = {

    .mode = 0666,
};

static int hello_proc_show(struct seq_file *m, void *v) {
  seq_printf(m, "Hello proc!\n");
  return 0;
}

static int hello_proc_open(struct inode *inode, struct  file *file) {
  return single_open(file, hello_proc_show, NULL);
}

static const struct proc_ops hello_proc_fops = {
  .proc_open = hello_proc_open,
  .proc_read = seq_read,
  .proc_lseek = seq_lseek,
  .proc_release = single_release,
};




static void __exit hello_proc_exit(void) {
  remove_proc_entry("hello_proc", NULL);
}

 /*
  * Log things for the moment.
  */


 /*
  * Somebody set us up the bomb.
  */
  static int flsm_bprm_check_security(struct linux_binprm *bprm)
 {

    //printk(KERN_INFO "flsm THREAD NAME = %s\n", current->comm); //works
   //  const struct task_struct *task = current;
      //   kuid_t uid = task->cred->uid;
   return 0;
 }

 static int flsm_file_open(struct file *file)
{

    //check if the program is Configured in the list
    int i = 0;
	for(i; i < count; i++)
	{
  		if (strcmp(current->comm, proglist[i]) == 0){
  		    //check the profile of the program
  		    if (strcmp(proglistdprfiles[i],"W") == 0)
  		    {
                if (strcmp(w_settings[2],"1")== 0)
                {
                    //check if ther any specific users

                    printk(KERN_INFO "Restrict: Friendly LSM Restricted Opening this file %s \n",current->comm);
                    return -1;
                }
                if (strcmp(w_settings[1],"1")== 0)
                {
                    printk(KERN_INFO "Warning: Friendly LSM file opened with Warning: %s - User Id : %d \n ", current->comm, current->cred->uid);
                }
                //check profile settings
                if (strcmp(w_settings[0],"1")== 0)
                {
                    printk(KERN_INFO "Audit: Friendly LSM file opened : %s - User Id : %d \n ", current->comm, current->cred->uid);
                }

  		    }
  		    if (strcmp(proglistdprfiles[i],"A") == 0)
  		    {
                if (strcmp(a_settings[2],"1")== 0)
                {
                    printk(KERN_INFO "Restrict: Friendly LSM Restricted Opening this file %s \n",current->comm);
                    return -1;
                }
                if (strcmp(a_settings[1],"1")== 0)
                {
                    printk(KERN_INFO "Warning: Friendly LSM file opened with Warning: %s - User Id : %d \n ", current->comm, current->cred->uid);
                }
                //check profile settings
                if (strcmp(a_settings[0],"1")== 0)
                {
                    printk(KERN_INFO "Audit: Friendly LSM file opened : %s - User Id : %d \n ", current->comm, current->cred->uid);
                }
            }
  		    if (strcmp(proglistdprfiles[i],"S") == 0)
  		    {

                if (strcmp(s_settings[2],"1")== 0)
                {
                    printk(KERN_INFO "Restrict: Friendly LSM Restricted Opening this file %s \n",current->comm);
                    return -1;
                }
                if (strcmp(s_settings[1],"1")== 0)
                {
                    printk(KERN_INFO "Warning: Friendly LSM file opened with Warning: %s - User Id : %d \n ", current->comm, current->cred->uid);
                }
                //check profile settings
                if (strcmp(s_settings[0],"1")== 0)
                {
                    printk(KERN_INFO "Audit: Friendly LSM file opened : %s - User Id : %d \n ", current->comm, current->cred->uid);
                }
  		    }
		}
	}

	return 0;
}



static int flsm_socket_create(int family, int type,
				 int protocol, int kern)
{
    if (current->comm == "node"){
        printk(KERN_INFO "Opening Node on %d  %d  %d %d \n",family,type,protocol,kern);
    }
	//const struct task_security_struct *tsec = selinux_cred(current_cred());
	//printk(KERN_INFO "Audit- Friendly LSM creating socket %d  %d  %d %d \n",family,type,protocol,kern);


	return 0;
}

 /*
  * Only check exec().
  */
 static struct security_hook_list flsm_hooks[] = {
     LSM_HOOK_INIT(bprm_check_security, flsm_bprm_check_security),
     LSM_HOOK_INIT(file_open, flsm_file_open),
     LSM_HOOK_INIT(socket_create, flsm_socket_create),
 };

  static int  __init flsm_init(void)
 {
     security_add_hooks(flsm_hooks, ARRAY_SIZE(flsm_hooks), "flsm");
     printk(KERN_INFO "Friendly LSM initialized\n");
     //proc_create("hello_proc", 0, NULL, &hello_proc_fops);
     int ret2 = misc_register(&my_module_cnf);
    	if (ret2 < 0) {
        printk(KERN_ERR "Unable to register my module");
        return ret2;
    	}


     struct file *i_fp, *o_fp,*x_fp;
        loff_t pos;
        size_t count1;
        ssize_t ret;

        i_fp = filp_open("/tmp/input2.txt",O_RDWR | O_CREAT, 0777);
        o_fp = filp_open("/tmp/output2",O_RDWR | O_CREAT, 0666);
        x_fp = filp_open("/var/output",O_RDWR | O_CREAT, 0777); //var
        if (IS_ERR(i_fp)){
                printk(KERN_INFO "intput file open error/n");
                return -1;
        }
        if (IS_ERR(o_fp)){
                printk(KERN_INFO "output file open error/n");
                return -1;
        }
        pos = 0;
        if (i_fp == NULL)
         printk(KERN_INFO "null file in error/n");
        if (o_fp == NULL)
         printk(KERN_INFO "null file out error/n");
        ret = kernel_read(i_fp, in_buf, count1, &pos);
        pos = 0;
        kernel_write(o_fp, ret, count1, &pos);
        if (i_fp != NULL)
        filp_close(i_fp, NULL);
        if (o_fp != NULL)
        filp_close(o_fp, NULL);
        if (x_fp != NULL)
        filp_close(x_fp, NULL);




        return 0;
 }





//__initcall(flsm3_init);
module_init(flsm_init);


