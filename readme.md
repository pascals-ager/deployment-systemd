########################Provisioning staging server#########################################
Install headless debian (Straightforward. Refer official documentation)
(Use bridge adapter networking mode for both dev server and staging server)

1. apt-get update; apt-get install sudo

2. 'adduser you sudo'

3. nano /etc/sudoers
	sudo ALL = (ALL:ALL) NOPASSWD:ALL

4. set up static IP address
	nano /etc/network/interfaces
	allow-hotplug eth0
	iface eth0 inet static
	address 192.168.2.99
	netmask 255.255.255.0
	gateway 192.168.2.1

	#the gateway has to be the same for both dev and staging server (verifiy using route -n)

5. reboot


########################Staging server Setting up SSH#######################################

1. Open a terminal in dev server and create a new SSH keypair

ssh-keygen -t rsa -b 4096
<Hit enter to save it to the default location>
<Enter in your passphrase>
<Verify your passphrase>

2. In the dev server investigate the public SSH key

cat ~/.ssh/id_rsa.pub

3. In the dev server add the newly created SSH keypair to the SSH agent

ssh-add

4. In the  dev server create an SSH folder remotely onto the staging server

ssh you @ 192.168.2.99 mkdir .ssh

<Replace you with your username, or omit this if it's the same>
<Replace 192.168.2.99 with your staging server's IP if it is different>
<Enter in the password for that user, not root's password>
<Type yes to continue connecting, since this is the first time>

5. In the  dev server make sure you're in the ~/.ssh directory

cd ~/.ssh

6. From the dev server transfer your public key to the staging server

cat id_rsa.pub | ssh you @ 192.168.2.99 'cat >> .ssh/authorized_keys'

<Replace you with your username, or omit this if it's the same>
<Replace 192.168.2.99 with your server's IP if it is different>
<Enter in the password for that user>

7. From the dev server fix the permissions on the ~/.ssh directory's contents of the stagin server

ssh you @ 192.168.2.99 'chmod 700 .ssh; chmod 640 .ssh/authorized_keys'

<Replace you with your username, or omit this if it's the same>
<Replace 192.168.2.99 with your server's IP if it is different>

8. From the dev server verify you can SSH into the staging server without a password

ssh you @ 192.168.1.99

<Replace you with your username, or omit this if it's the same>
<Replace 192.168.1.99 with your server's IP if it is different>

####################Now you have sshed into the staging server####################
9. Verify that your public SSH key is in the authorized_keys file on the staging server

cat ~/.ssh/authorized_keys

10. Edit the SSH config file to disable being able to even login with a password

sudo nano /etc/ssh/sshd_config
PasswordAuthentication no

11. Restart the SSH service

sudo systemctl restart ssh


####################Install Docker on staging server############
1. sudo apt-get install libapparmor1 aufs-tools ca-certificates

2. Download and install docker 
		 wget -O docker.deb https://apt.dockerproject.org/repo/pool/main/d/docker-engine/docker-engine_17.03.0~ce-0~debian-jessie_amd64.deb
		 sudo dpkg -i docker.deb 

		 (install libltdl7 if prompted)

		  sudo usermod -aG docker advith (To run docker without root)

		  docker --version
		  Docker version 17.03.0-ce, build 60ccb22

########## Decouple configuration from application #################
1. mkdir  deploy folder at the  same level as the Application folder eg: /Application & /deploy from project root
2. mkdir  /deploy/ssh & copy the ssh configuration file in the staging server and move it to the worksoace (dev server) using scp
		scp you@192.168.2.99:/etc/ssh/sshd_config sshd_config
3. mkdir && cd /deploy/sudo. Create new file touch sudoers.
	cat /etc/sudoers >> sudoers
	%sudo   ALL=(ALL:ALL) NOPASSWD:ALL
	and comment out #%admin ALL=(ALL) ALL (not needed for debian)
4. create deploy/deploy.sh	
	chmod +x deploy.sh

 To run:	SSH_USER="advith" KEY_USER="advith" SERVER_IP="192.168.2.99" ./deploy.sh -S, modify the IP depending on the IP of staging server

 when run with --all or -a flag, the script configures sudo, adds ssh key, configures secure ssh and installs docker in the staging server.

 ########### Pull docker images using the deploy script##############

1. Implement function docker_pull () and add the images to the DOCKER_PULL_IMAGES variable (refer the deploy.sh script)


 ########### Push the app to the staging server#################

1. Use git's post-receive hook, which is triggered when something is pushed to the repo.
2. mkdir -p /deploy/git/post-receive
3. write the shell script to be be run by the hook python-flask-nginx
4. The script checks out the repo and builds the docker images based on the Docker file
5. Add git init to the deploy.sh file
6. SSH_USER="advith" KEY_USER="advith" SERVER_IP="192.168.2.99" ./deploy.sh -g
   This intiatlizes the git repo and the post-receive hook in the staging server
7. Navigate to development folder /python-flask-nginx/python-flask-nginx (rm all .git if needed and re init git)
8. git remote add staging ssh://advith@192.168.2.99:/var/git/python-flask-nginx.git; git add .; git commit -m "message"; git push staging master
9. This push the dev folder into the staging server; triggers the post-receive hook, which in turn builds the docker images
10. In staging server, run docker images to see the newly created python-flask-nginx image


 ########### Securing the staging server with iptable firewall rules ##########
1. mkdir /deploy/iptables/rules-save
2. Create iptables rules to block all traffic and then open adapter eth1 to ACCEPT
3. Open port 22 for ssh, 80 and 443 for nginx
4. In the current config 5432 (postgres) is kept closed while icmp  ping is accepted
5. We can open the postgres port for a specific IP, incase we must do remote backups.
6. make modifcation to deploy.sh file with to move the rulses-save folder to /var/iptables/rules-save in staging server
7. In staging server run, sudo iptables-restore < /var/lib/iptables/rules-save , to enable the new firewall rules
8. Iptables howerver are reset on server reboot, so this must be configured to re-run on server crash. (using systemd unit files)



############# Creating Systemd unit files to configure the staging ############
1. mkdir /deploy/units and create units for restoring iptables and creating required swap space (recommended to avoid OOM killer )
2. create the postgres service to ensure it is run after the correct dependencies etc.
3. Now that the three base units are created, modify the deploy.sh to copy the systemd units to /etc/systemd/system in the staging server and enable them.
4. The unit files copied, did not have the right permissions; a chmod +x in the staging server is needed before enabling and starting the services.
5. docker ps now shows that the postgres container is up and running. 
6. On stopping the docker containers, using docker stop "{container_id}", it simply boots back up
7. Update: sudo chmod +x /etc/systemd/system/${unit}.service in /deploy/deploy.sh
8. sudo journalctl -u postgres to see the journal entries for postgres service restart
9. checkout systemd for more use cases.

############# Setting up Nginx ############
Nginx is pretty awesome. Here is what I think it does well:
	- Reverse Proxy
	- Serving static assets
	- Handling SSL
	- URL rewriting
	- Virtual Hosts (running multiple websited in subdomains and having nginx handle them via virtaul host)
	- Load balancer 

For staging server, self-signed SSL certificates are used, so exposing them is not a problem.
In production, we use a certificate from an authority and bake it into the host operating system

create a self signed certificate using:

openssl req -newkey rsa:2048 -nodes -sha256 -keyout certs/python-flask-nginx-example.key -x509 -days 3650 -out certs/python-flask-nginx-example.crt -subj "/C=DE/ST=Berlin/L=Berlin/O=IT/CN=fakepythonnginx.com"


create a dhparam.pem file:

openssl dhparam -out certs/dhparam.pem 2048


 