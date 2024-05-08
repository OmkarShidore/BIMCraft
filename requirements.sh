#Debian dependencies
sudo apt install libpq-dev -y
sudo apt install -y postgresql-common
echo -e '\n' | sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh
sudo apt install postgresql-15-pgvector
sudo apt-get install libp11-kit0

#Python dependencies
pip install --upgrade pip
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt