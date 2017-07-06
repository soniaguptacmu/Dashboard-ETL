# Kolibri-ETL

# creating virtual env
python3 -m venv /Users/soniagupta/desktop/sem3/studio/DataFetcher/Kolibri-ETL
source bin/activate

# installing package using pip3 
pip3 install sqlalchemy
pip3 install schedule
pip3 install PyMySQL

# creating requirments.txt file which will have all dependencies that you installed using pip3 install
pip3 freeze > requirements.txt

# installing all packages using requirements.txt
pip3 install -r requirements.txt
