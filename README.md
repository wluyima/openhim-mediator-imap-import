[![OpenHIM Core](https://img.shields.io/badge/openhim--core-1.5%2B-brightgreen.svg)](http://openhim.readthedocs.org/en/latest/user-guide/versioning.html)

# openhim-mediator-imap-import
OpenHIM Mediator for handling user requests to import indicator mappings in OCL. 

## installation

- Git clone the repository  into `/usr/share/`
- `sudo vim /usr/share/openhim-mediator-imap-import/config/default.json` to change the config as needed.
- `sudo vim /etc/init/openhim-mediator-imap-import.conf `
```
# OpenHIM imap-import mediator

description "OpenHIM imap-import mediator"

# logs to /var/log/upstart/openhim-mediator-imap-import.log
console log

start on runlevel [2345]
stop on runlevel [!2345]

respawn

setuid openhim
setgid openhim

script
 # export PATH=/home/openhim/.nvm/versions/node/v0.12.7/bin/:$PATH
  export NODE_TLS_REJECT_UNAUTHORIZED=0
  cd /usr/share/openhim-mediator-imap-import
  exec bash -c "source /home/openhim/.nvm/nvm.sh && nvm use 4 && npm start"
end script
```
- cd /usr/share/openhim-mediator-imap-import
- sudo  npm install
- sudo chown -R openhim:openhim /usr/share/openhim-mediator-imap-import/
- Start the mediator with `sudo service openhim-mediator-imap-import start`
- restart or stop the mediator with `sudo service openhim-mediator-imap-import restart` or `sudo service openhim-mediator-imap-import stop`
- Logs are available at - `/var/log/upstart/openhim-mediator-imap-import.log`

Now you can setup your HIM channels and the mediator config via the console.

## Polling Channel Example
Say we have a maintenance script `task.sh` that needs to execute on a daily basis. Copy the script into the mediator scripts directory and give it execute permission:
```
cp task.sh /opt/openhim-imap-import
chmod +x /opt/openhim-imap-import/task.sh
```
Note that the mediator *process* needs execute permission for the script.

With the script in place we can setup the channel and mediator in console. Go to *Mediators* and click on the *OpenHIM imap import Mediator* item. From there click on the blue *Configure Mediator* button.

Add a new script and give it an endpoint on which to trigger execution. Enter the name of the script `task.sh`. Any required arguments or environment variables can be added as well.
![screen shot 2016-03-10 at 09 12 34](https://cloud.githubusercontent.com/assets/1872071/13662056/4ab49908-e6a0-11e5-90d3-bb10298bf95b.png)

After you hit the *Save Changes* button, the mediator will automatically pick up on the new config.

Now we can setup a new channel that will call the script on a daily basis. Add a new polling channel:
![channel-basic-info](https://cloud.githubusercontent.com/assets/1872071/13661621/f0066d2c-e69c-11e5-9e8c-b7b7ad5c15b8.png)

Give it an access control permission such as `internal`.

Add the script route by picking the *OpenHIM imap import Mediator* option in *Add Mediator Route*. Edit the route and set *Route Path* to `/task`:
![channel-route](https://cloud.githubusercontent.com/assets/1872071/13661539/0907ab20-e69c-11e5-807a-d82ac6339dc1.png)

Click on *Save Changes* and then that's it. The polling channel will now execute the script daily. The script output (both `STDOUT` and `STDERR`) will be viewable in the response body for the transaction.


## License
This software is licensed under the Mozilla Public License Version 2.0.
