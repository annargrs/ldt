===============
Troubleshooting
===============

------------------------------------
Wrong location of configuration file
------------------------------------

If LDT loads sample configuration file instead of the configuration file in the user home folder, check if you have unittests or sphinx loaded in sys.modules. If you do, you can remove them with `del sys.modules["unittest"]`


