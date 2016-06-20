A sublime plugin to sync code written in an Ipython notebook cell (when using the %%file magic function).

When one defines a file in Ipython notebook using the %%file magic function, and then edit the file, the file on the disk is overwritten. This is one way syncing available inherently in Ipython notebook.
This plugin facilitates the second way syncing (i.e writing code in Sublime text, and then syncing it so that the change is reflected in the Ipython notebook).

When this plugin is run (can be done by simply binding a key combination for running this plugin), the plugin will look at the file that is currently being edited in sublime text (lets say foo.py) and at Ipython notebooks in the current working directory and if it finds a cell consisting of "%%file foo.py" in that notebook, it will replace the code in the cell with the code in the foo.py file selected in sublime text.