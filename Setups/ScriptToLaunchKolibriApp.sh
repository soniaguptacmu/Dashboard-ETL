#download pex file
Wget https://github.com/learningequality/kolibri/releases/download/v0.4.0-beta10/kolibri-v0.4.0-beta10.pex
 
# make the pex file executable
chmod +x kolibri-v0.4.0-beta10.pex
 
#import a test channel
./kolibri-v0.4.0-beta10.pex manage importchannel -- network eb99f209f9c34ba192f6e695aeb37e4f
./kolibri-v0.4.0-beta10.pex manage importcontent -- network eb99f209f9c34ba192f6e695aeb37e4f

# start the server after which the server will be launched at port localhost:8080 
./kolibri-v0.4.0-beta10.pex start
