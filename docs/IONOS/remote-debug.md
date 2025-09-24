# Remote debugging

## Coarse steps

1. In IDE enable and start debug server with proper path mapping
2. In Open WebUI load and run a debug module (i.e. `pydevd`)


## Pycharm or other IntelliJ products

### Find debug server port in IDE

1. Open burger (main) menu
2. Click **Settings**
3. In settings go to **Build, Execution, Deployment > Debugger**
4. Find the **built-in server** port

### Setup debugger

1. Open burger (main) menu
2. Click **Run**
3. Click **Debug configurations**
4. In the dialog click the **plus** icon
5. Choose **Python debug server** from the menu
6. Enter host name `127.0.0.1`
7. Enter port name `64999` (example)
8. Enter your path mapping in the form `<HOSTPATH>=`

### Load `pydevd` in code

Attach to the backend container and run:

```
pip install pydevd pydevd-pycharm~=243.23654.177
```

**You have to do this after every dev container restart!**

In `backend/open_webui/main.py` insert this:

```
import pydevd_pycharm
pydevd_pycharm.settrace('127.0.0.1', port=64999, stdoutToServer=True, stderrToServer=True)
```

The port number has to be changed to something your IDE uses.

### Troubleshooting debugging with Pycharm

#### Does not stop at breakpoints

See also: next problem below.

##### Problem and symptoms

1. Pycharm console shows the debugger is running and I can see the red and gree buttons
2. Code is definitively executed, but the debuuger does not start

##### Verification steps

2. Ensure the debugger process is started in the application
   * Double check you run the debugger
   * Look for log messages like `0.00s - Note: Debugging will proceed.`
2. In the Pycham status bar it should not show "waiting for connection"



#### `Trying to add breakpoint to file that does not exist`

##### Problem

Debugger attached, redirects logs to the Pycharm console, but does not stop at breakpoints.

##### Symptoms

Logged to the Pycharm console:

```
ydev debugger: Trying to add breakpoint to file that does not exist: <host path> (will have no effect).
```

##### Verification steps

1. Verify the logged path really exists using `ls` for example
2. If you the host path goes through a symlink at one level this may confuse Pycharm
   Try opening the file from the non-symlinked path.


## See also

https://www.jetbrains.com/help/pycharm/remote-debugging-with-product.html
