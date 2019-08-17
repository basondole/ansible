Ansible uses playboooks to perform tasks.
A play book consists of one or more tasks to be performed by modules
There are different modules for different operations such as copying files, sending shell comands etc
These tasks are performed against specified host(s) as specified in the play
Generaly however the hosts must be defined in the ansible hosts file
A simple task can also be executed by using ad-hoc command, this means no play book is required and the command can be simply run on terminal specifying the module to use and the host(s)

Example of ad-hoc command:

baggy@plasma:~/ansible$ cat hosts
[routers]
192.168.56.36 ansible_network_os=junos ansible_ssh_user=fisi  ansible_ssh_password=fisi123

baggy@plasma:~/ansible$

baggy@plasma:~/ansible$ ansible -m raw -a "show system alarms" 192.168.56.36 -i ./hosts
192.168.56.36 | SUCCESS | rc=0 >>
No alarms currently active
Shared connection to 192.168.56.36 closed.



baggy@plasma:~/ansible -m junos_command -a "commands='show syst alarm'" -c network_cli 192.168.56.36
 [WARNING]: arguments wait_for, match, rpcs are not supported when using transport=cli

192.168.56.36 | SUCCESS => {
    "changed": false,
    "stdout": [
        "show system alarms \nNo alarms currently active"
    ],
    "stdout_lines": [
        [
            "show system alarms ",
            "No alarms currently active"
        ]
    ]
}

Example of a playbook:

baggy@plasma:~/ansible$ cat hosts
[routers]
192.168.56.36 ansible_network_os=junos
192.168.56.26 ansible_network_os=ios
baggy@plasma:~/ansible$

<pre>
baggy@plasma:~/ansible$ cat uptime.yml
---
   - hosts: routers
     gather_facts: no
     ignore_errors: yes
     vars:
        ansible_ssh_user: fisi
        ansible_ssh_password: fisi123

     tasks:
         - name: check uptime juniper
           raw: show system uptime | match boot
           register: junos_uptime
           when: ansible_network_os == "junos"

         - name: check uptime cisco
           raw: show ver | i uptime
           register: cisco_uptime
           when: ansible_network_os == "ios"

         - name: print the uptime
           debug: var=junos_uptime.stdout
           debug: msg="{{ cisco_uptime.stdout }}"
baggy@plasma:~/ansible$
</pre>



Get more information about a module
baggy@plasma:~/ansible$ ansible-doc <module name>


Check what documentation is availbale 
baggy@plasma:~/ansible$ ansible-doc -l

