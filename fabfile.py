from fabric.api import *

# Keyfile for SSH.
env.key_filename = "~/.ssh/hpcompute.pem"

@task
def hello():
    puts("Hello")

@task
def create_server(name):
    """Create a new HP Cloud server."""
    image = 81078 # Ubuntu 12.04 in AZ-1
    flavor = 100  # extra-small
    security_group = 'Web'
    key = 'hpcompute'

    # This is the local command we'll run.
    template = "hpcloud servers:add %s %s -i %s -k %s -s %s"
    cmd = template % (name, flavor, image, key, security_group)

    local(cmd)

@task
def destroy_server(name):
    """Destroy an HP Cloud server."""
    local("hpcloud servers:remove %s" % name)

@task
def server_details(name = ''):
    """Get the server details."""
    local("hpcloud servers %s" % name)

@task
def install_lamp():
    """Install a LAMP stack on the server."""

    # Install the packages
    sudo("apt-get -q update")
    packages = "apache2 mysql-server libapache2-mod-php5 php5-mysql"
    sudo("apt-get install -q %s" % packages)

    # Push the index.php file to the server and get rid of
    # the old index.html file.
    put("index.php", "/var/www/index.php", use_sudo=True)
    sudo("rm /var/www/index.html")
