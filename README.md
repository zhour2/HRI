MyOpenHMI
*This is my work based on the openHMI*

**Author: Richard Zhou**

**Email: zhour2@rose-hulman.edu**

# 1. Raspberry Pi Setup
## 1.1 Make System Image with Raspberry Pi Imager.
+ Raspberry Pi Imager can be downloaded via: https://www.raspberrypi.com/software/

![](https://raw.githubusercontent.com/CNlaochen/PicGo/main/rpiImagerDownload.png)

+ Insert SD card onto the PC and launch Raspberry Pi Imager.
+ Choose OS as "**Raspberry Pi OS (64bit)**"
![](https://raw.githubusercontent.com/CNlaochen/PicGo/main/selectOS.png)
+ Then choose storage (***Not necessarily a large SD card, 16GB is enough***)
![](https://raw.githubusercontent.com/CNlaochen/PicGo/main/selectStorage.png)
+ Click "**WRITE**" to launch the image download and write process. The images will firstly download the image, then write to SD card and finally check the written binaries. When everything is ok, the SD card is ready to use.
![](https://raw.githubusercontent.com/CNlaochen/PicGo/main/writeSDDone.png)

## 1.2 Raspberry Pi HW setup
+ Connect Mouse and Keyboard via USB port.
+ Connect U2D2 Adapter via USB port. (Skip this step if you don't have Blossom Robot)
+ Connect Camera via the Camera port on the board. (Skip this step if you don't have Camera) 
+ Connect display monitor via the mini HDMI port (May need a mini HDMI to HDMI adapter if you only have an HDMI cable)
+ Insert the SD card into the SD socket.
+ Connect the power supply via the Type-C port.
## 1.3 Configure OS and package source repository
+ When the system boots up for the very first time, the it would require user to specify some key informations such as user name and password, time, time zone, localization, and keyboard, etc.
+ **For China's users only**. You would most probabaly experience a very slow package downloading due to the network issue. Then you need to configure the package source repo to a mirror located in mainland China. There are several mirrors avaialbe to use. Refers to: https://blog.csdn.net/zifengzwz/article/details/107922635
+ Set the password of root: Open the terminal and then input the following command:

**This step is only needed to executed for the very first time you'd like to run a command with sudo**

```shell
sudo passwd root
```
Then the system will ask you to input the initial password.
```shell
Enter new UNIX passwoord: 
Retype new UNIX password:
```
## 1.4 Download the essential SWs
Open the terminal, and follow the steps.
+ Update the repo
```shell
sudo apt-get update
```
+ Upgrade the installed softwares
```shell
sudo apt-get upgrade
```
This step would take pretty long time, just wait for the accomplishment.
+ Install all the dependencies
```shell
sudo apt-get install build-essential libssl-dev libffi-dev python3-dev xvfb ca-certificates curl gnupg git
```
# 2. Fetch the Project
You can fetch the project either via git or directly copy from shared folder or external storage.

The structure of the porject source is as follows:
![](https://raw.githubusercontent.com/CNlaochen/PicGo/main/project_arch.png)

+ requirements.txt: This is all the python packages needed in order to run the project.
+ gears_up.sh: This script is launching the python virtual enrivonment.
+ Utility: This folder contains all the utilities needed such as FrameCapture for dataset capturing.
+ EnvTest: This folder contains the test programs to assure the HW is working appropriately.
+ HGR: This folder contains the Hand Gesture Recognition application.
+ blossom: This folder contains all the stuffs for the Robot control.

## 2.1 Launch the Python venv (Need to run every time a new terminal is opened)
```shell
source ./gears_up.sh
```
## 2.2 Install the pythohn dependencies (Only need to execute when the project is initially downloaded)
** NOTE: For China's Users, due to the network issue, mirror site is suggested to be specified with the following command. Let's take an example of using https://pypi.tuna.tsinghua.edu.cn/simple/

The following commands are executed on the top-level of the project.

+ For non-China's users:
```shell
pip install -r requirements.txt
```
+ For China's users:
```shell
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

```

# 3. Development
# 3.1 Test functionality of Camera
It is strong suggested to test the functionality of the Camera before everying sterts.
For the convenience of developing, I recommend using VSCode. Make life easier. :)
You can find VSCode installer via: https://code.visualstudio.com/download
You need to download the type of .deb (Arm64) if you're using Raspberry Pi 4+.
If you have decided to use VSCode, you can simply launch the VSCode on the top-level of the project.
```shell
code .
```
Then you can check the running environment is already set as python-venv on the bottom-right corner of the VSCode.
In order to test the functionality of the Camera, you need to run <myopenhmi>/EnvTest/test_camera_v2.py.
This program test to preview the camera in 3 modes, in which it last 5 seconds. If no error pops up and you can see the preview window, camera is ok.