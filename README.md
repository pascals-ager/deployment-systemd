# deployment-systemd
Deployment scripts to configure passwordless sudo, ssh,  iptables, self-signed certificates, nginx and also set up application, postgres, and nginx as an on-boot service in a remote server using systemd. Also contains git post-receive hooks to trigger builds on push to remote git repository.


Usage: ${0} (-h | -S | -u | -k | -s | -d [docker_ver] | -l | -g | -f | -c | -b | -e | -x | -r | -a [docker_ver])
ENVIRONMENT VARIABLES:
   SERVER_IP        IP address to work on, ie. staging or production
                    Defaulting to ${SERVER_IP}
   SSH_USER         User account to ssh and scp in as
                    Defaulting to ${SSH_USER}
   KEY_USER         User account linked to the SSH key
                    Defaulting to ${KEY_USER}
   DOCKER_VERSION   Docker version to install
                    Defaulting to ${DOCKER_VERSION}
OPTIONS:
   -h|--help                 Show this message
   -S|--preseed-staging      Preseed intructions for the staging server
   -u|--sudo                 Configure passwordless sudo
   -k|--ssh-key              Add SSH key
   -s|--ssh                  Configure secure SSH
   -d|--docker               Install Docker
   -l|--docker-pull          Pull necessary Docker images 
   -g|--git-init             Install and initialize git 
   -f|--firewall             Configure the iptables firewall
   -c|--copy--units          Copy systemd unit files
   -b|--enable-base-units    Enable base systemd unit files
   -e|--copy--environment    Copy app environment/config files
   -x|--ssl-certs            Copy SSL certificates
   -r|--run-app              Run the application   
   -a|--all                  Provision everything except preseeding
EXAMPLES:
   Configure passwordless sudo:
        $ deploy -u
   Add SSH key:
        $ deploy -k
   Configure secure SSH:
        $ deploy -s
   Install Docker v${DOCKER_VERSION}:
        $ deploy -d
    
    Pull necessary Docker images:
        $ deploy -l
   Install and initialize git:
        $ deploy -g        
   Configure the iptables firewall:
        $ deploy -f
   Copy systemd unit files:
        $ deploy -c
   Enable base systemd unit files:
        $ deploy -b
   Copy app environment/config files:
        $ deploy -e
   Copy SSL certificates:
        $ deploy -x
   Run the application:
        $ deploy -r       
   Configure everything together:
        $ deploy -a
   Configure everything together with a custom Docker version:
        $ deploy -a 17.03.0
