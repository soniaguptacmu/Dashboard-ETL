#download pex file
Wget https://github.com/learningequality/kolibri/releases/download/v0.4.0-beta10/kolibri-v0.4.0-beta10.pex
 
# make the pex file executable
chmod +x kolibri-v0.4.0-beta10.pex
 
#import a test channel
./kolibri-v0.4.0-beta10.pex manage importchannel -- network abb42df1203f4043a7b6e430de257d90
 
# start the server after which the server will be launched at port localhost:8080 
./kolibri-v0.4.0-beta10.pex start
