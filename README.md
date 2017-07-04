## CITC LAB - Simple Blood Test App 
CAUTION: It designed for Learning/Fun Puspose. Don't use it for production.

----

### Installation
- **Ubuntu 16.04.2**:
```
# Prepare system for the project
sudo apt-get update
sudo apt-get install -y python-dev libmysqlclient-dev

wget https://bootstrap.pypa.io/get-pip.py
sudo -H python get-pip.py
sudo -H pip install virtualenv

# Configure the locale if needed
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# Clone the project
git clone https://github.com/devahmedshendy/citc_lab.git

# Initialize/Active a virtual environment
cd citc_lab
virtualenv venv
source venv/bin/activate # for Bash Shell
. venv/bin/activate.fish # Fish Shell

# Install the requirements for the project
pip install -r requirements.txt

# Create the database
python initialize-db.py
python run.py

# Now you can access the application from browser
http://localost:5000
username: admin
password: admin
```
