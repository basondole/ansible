# Readme

Ansible is an open-source automation tool, or platform, used for IT tasks such as configuration management, application deployment, intraservice orchestration and provisioning.
Learn more at www.ansible.com  
Ansible uses playbooks to perform tasks. Essentially a play book consists of one or more tasks to be performed by modules
There are different modules for different operations such as copying files, sending shell comands etc
These tasks are performed against specified host(s) as specified in the play.
Generaly however the hosts must be defined in the ansible hosts file
A simple task can also be executed by using ad-hoc command, this means no play book is required and the command can be simply run on terminal specifying the module to use and the host(s)

First we have to create the invetory file for our devices
<pre>
baggy@plasma:~/ansible$ cat hosts
[routers]
192.168.56.36 ansible_network_os=junos ansible_ssh_user=fisi  ansible_ssh_password=fisi123
192.168.56.26 ansible_network_os=ios ansible_ssh_user=fisi  ansible_ssh_password=fisi123
</pre>


## ad-hoc commands
In below examples we are issuing the `show system alarms` commnad to a junos device using two different modules
thats is the `raw` module and the `junos_command` module  
<pre>
baggy@plasma:~/ansible$ ansible -m raw -a "show system alarms" 192.168.56.36 -i ./hosts
192.168.56.36 | SUCCESS | rc=0 >>
<b>No alarms currently active</b>
Shared connection to 192.168.56.36 closed.
</pre>

<pre>
baggy@plasma:~/ansible -m junos_command -a "commands='show syst alarm'" -c network_cli 192.168.56.36 -i ./hosts
 [WARNING]: arguments wait_for, match, rpcs are not supported when using transport=cli

192.168.56.36 | SUCCESS => {
    "changed": false,
    "stdout": [
        "show system alarms \nNo alarms currently active"
    ],
    "stdout_lines": [
        [
            "show system alarms ",
            <b>"No alarms currently active"</b>
        ]
    ]
}
</pre>

## Playbook

In the example below a playbook runs and gets the uptime of junos and cisco ios device

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

</pre>

### Playing the book

<pre>
baggy@plasma:~/ansible$ ansible-playbook router_uptime_playbook.yml  -i hosts  -v            
Using /etc/ansible/ansible.cfg as config file

PLAY [routers] ********************************************************************************

TASK [check uptime juniper] *******************************************************************
skipping: [41.188.128.41] => changed=false
  skip_reason: Conditional result was False
changed: [41.188.128.120] => changed=true
  rc: 0
  stderr: |-
    Shared connection to 41.188.128.120 closed.
  stdout: |-
    <b>System booted: 2019-05-21 16:38:27 EAT (12w3d 23:26 ago)</b>
  stdout_lines: <omitted>

TASK [check uptime cisco] *********************************************************************
skipping: [41.188.128.120] => changed=false
  skip_reason: Conditional result was False
changed: [41.188.128.41] => changed=true
  rc: 0
  stderr: |-
    Shared connection to 41.188.128.41 closed.
  stdout: |-
    <b>router01 uptime is 22 weeks, 2 days, 6 hours, 27 minutes</b>
  stdout_lines: <omitted>

PLAY RECAP ************************************************************************************
41.188.128.120             : ok=1    changed=1    unreachable=0    failed=0
41.188.128.41              : ok=1    changed=1    unreachable=0    failed=0
</pre>

After a playbook completes you get a recap of the tasks done

To get more information about a module  
`baggy@plasma:~/ansible$ ansible-doc <module name>`


To check what documentation is availbale  
`baggy@plasma:~/ansible$ ansible-doc -l`

