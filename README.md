# Kolibri-ETL

# Process for setting the environment on local

Step1: creating virtual environment.

virtualenv --no-site-packages mydjangoappvenv

source mydjangoappvenv/bin/activate

Step 2: installing all packages using requirements.txt

pip3 install -r requirements.txt


# Process of managing dependency during Development

Step 1: installing package using pip3 

pip3 install package_name

Step 2: creating a dependency file

pip3 freeze > requirements.txt

