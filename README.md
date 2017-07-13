# Kolibri-ETL

####### Process for setting the environment on local

# creating virtual environment

virtualenv --no-site-packages mydjangoappvenv

source mydjangoappvenv/bin/activate

# installing all packages using requirements.txt

pip3 install -r requirements.txt


####### During Development

# installing package using pip3 

pip3 install sqlalchemy

pip3 install schedule

pip3 install PyMySQL

# creating a dependency file

pip3 freeze > requirements.txt

