# Install Steps
´´´
sudo apt update
sudo apt upgrade
sudo apt install -y mininet
´´´

or

´´´
git clone https://github.com/mininet/mininet.git
cd mininet
sudo ./util/install.sh -a
´´´

# Test if install was successfull
mn --test pingall

or 

python3 -c "import mininet; print(mininet.__file__)"

# How to run
sudo python3 main.py