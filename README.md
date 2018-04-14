# VTCA - Virginia Tech Course Alerter
A web application which allows you to create a .txt file containing Virginia Tech courses you select. The generated .txt file can be used with the provided python script (listen.py) to create a desktop alert when there is an availability in a course. The checking interval can be modified (default of 10 seconds).

## Installation
1. Download and install [Python](https://www.python.org/downloads/) 
2. Set up Python environment variables (in Windows)
    1. Control Panel &gt; System &gt; Advanced System Settings &gt; Environment Variables
    2. Under System variables, click New...
    3. For variable name, enter PYTHONPATH
    4. For variable value, enter the path at which you installed Python (ie. C:\Python36)
3. Enter 'pip install py-vt' in command prompt
 
## Usage
### Classes
1. Open index.html in your preferred browser
2. Add the courses you want to wait for openings using the interface
3. Click on 'Save File' button (this should download a file named listening_list.txt
4. Move downloaded file to VTCA folder

### Script
1. Run command prompt or some shell
2. #### Set working directory to VTCA folder
   ##### Example, assuming VTCA folder on desktop:
    ```
    cd Desktop/VTCA
    ```
3. Run the listen.py script: 
    ```
    python listen.py
    ```
    
To see a more detailed usage:
```
python listen.py -h
```

## Problems
Currently, there are no known problems.

## Alternatives
### [Course Pickle](https://coursepickle.com/)
  Well known service for notifying Virginia Tech students about course openings. Less work required to setup compared to my alternative. However, non-premium notifications are delayed 5-10 minutes. That information along with unknown opening checking intervals, may result in missed opportunities.
  
### [Coursicle](https://www.coursicle.com/)
  Similar to Course Pickle. Differences are Coursicle supports text messaging by default, but requires payment for adding multiple classes to listen to. Opening checking intervals are unknown to me.

### [Timetable Stalker](https://github.com/amhokies/Timetable-Stalker)
  Great alternative for notifying course openings. Utilizes Pushbullet to send notifications to all devices. My previous experiences with Pushbullet showed that the notifications were delayed, however this was just my experience (and I used it some time ago). All you need is Python installed.
