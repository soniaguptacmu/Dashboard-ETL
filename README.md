# Kolibri-ETL

# creating virtual environment
python3 -m venv ../Kolibri-ETL
source bin/activate

# installing package using pip3 
pip3 install sqlalchemy
pip3 install schedule
pip3 install PyMySQL

# creating a dependency file
pip3 freeze > requirements.txt

# installing all packages using requirements.txt
pip3 install -r requirements.txt
