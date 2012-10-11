## rx82xx Remote - A scheduled remote control for the Ericsson 8200 IRD 

##### Warning: This is the first thing I have written using Django (Python really). If you choose to use it in production you are doing so at your own risk! There are likely bugs. This has been developed for and tested with the Ericsson 8200 Receiver deployed to many public television stations. It may work with the 8252 as well, but we do not have one on-site to confirm.

### Requirements
* [Python 2.x](http://python.org)
* [Django](https://www.djangoproject.com/)
* [APScheduler](http://packages.python.org/APScheduler/)
* [PySNMP](http://pysnmp.sourceforge.net/)
* [CherryPy](http://www.cherrypy.org/) (if using built in webserver)

### Installation
* Install requirements.
* Edit ericsson_remote/settings.py to match your receiver info and tuning requirements
* Start dispatcher.py
* Start runserver.py (or other webserver)
* Visit http://your_server:8000

### Usage
* Add an event by setting the date/time, receiver and schedule to tune
* You can edit or delete existing events in the future
* The receiver will change to the selected schedule at the specified time

### Limitations
* Jobs are added to the jobstore using a polling mechanism, so there may be up to a 10 second delay between the time a job is added in the UI and it is actually scheduled
* Job execution time is only as accurate as the clock on the system running dispatcher.py
* There is currently no authentication mechanism

### License
This is open-sourced software licensed under the MIT License.