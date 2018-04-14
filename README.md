<h1>VTCA - Virginia Tech Course Alerter</h1>
<p>
A web application which allows you to create a .txt file containing Virginia Tech courses you select. The generated .txt file can be used with the provided python script (listen.py) to create a desktop alert when there is an availability in a course. The checking interval can be modified (default of 10 seconds).
</p>

<h2>Installation</h2>
<ol>
  <li>Download and install <a href="https://www.python.org/downloads/">Python</a></li>
  <li>
    Set up Python environment variables (in Windows)
    <ol>
      <li>Control Panel &gt; System &gt; Advanced System Settings &gt; Environment Variables</li>
      <li>Under System variables, click New...</li>
      <li>For variable name, enter PYTHONPATH</li>
      <li>For variable value, enter the path at which you installed Python (ie. C:\Python36)</li>
    </ol>
  </li>
  <li>Enter 'pip install py-vt' in command prompt</li>
</ol>
 
<h2>Usage</h2>
<p>
  Open index.html in your browser. Add the courses you want to wait for opening in. Once finished adding all desired courses, click on 'Save File' button (this should download a file named listening_list.txt) Move listening_list to the folder (named VTCA-master by default) containing the provided files. Run command prompt. Change path to VTCA-master. Assuming, command prompt displays: C:\Users\USER>, enter the command 'cd Desktop\VTCA-master' if you moved VTCA-master to your desktop. Finally, run the provided python file with 'python listen.py -d', where -d is replaced with a number for the delay for course availability checking (in seconds). To exit, press Ctrl+C or Ctrl+Z or exit command prompt.
</p>

<h2>Problems</h2>
<p>
  Currently there are no unknown problems.
</p>

<h2>Alternatives</h2>
<a href="https://coursepickle.com/">Course Pickle</a>
<p>
  Well known service for notifying Virginia Tech students about course openings. Less work required to setup compared to my alternative. However, non-premium notifications are delayed 5-10 minutes. That information along with unknown opening checking intervals, may result in missed opportunities.
</p>
<a href="https://www.coursicle.com/">Coursicle</a>
<p>
  Similar to Course Pickle. Differences are Coursicle supports text messaging by default, but requires payment for adding multiple classes to listen to. Opening checking intervals are unknown to me.
</p>
<a href="https://github.com/amhokies/Timetable-Stalker">Timetable Stalker</a>
<p>
  Great alternative for notifying course openings. Utilizes Pushbullet to send notifications to all devices. My previous experiences with Pushbullet showed that the notifications were delayed, however this was just my experience (and I used it some time ago). All you need is Python installed.
</p>
