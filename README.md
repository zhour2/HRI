MyOpenHMI
*This is my work based on the openHMI*
**Author: Richard Zhou**
**Email: zhour2@rose-hulman.edu**

# 0 Setup & Initial Configuration

## 0.1 SW Environment Setup

### 0.1.1 Install pip3

```shell
sudo apt install python3-pip
```

### 0.1.2 Install virtual environment (venv)

```shell
sudo apt-get install python3-venv
```

### 0.1.3 Get everything well-prepared
```shell
source ./gears_up.sh
```

### 0.1.4 General Setup

```shell
sudo apt-get install build-essential libssl-dev libffi-dev python3-dev xvfb ca-certificates curl gnupg
pip install wheel
```

### 0.1.5 Install Requirements

```shell
pip install -r requirements.txt
```

**NOTE**: Under some extreme circumstances, there might be inconsistent hashes issue reported so that the installation is blocked.

Try this:

```she
pip install --no-cache-dir -r requirements.txt
```

### 0.1.6 Install nodejs

#### Step-1: Download and import the Nodesource GPG key

```sh
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
```

#### Step-2: Create deb repository

```sh
NODE_MAJOR=20
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list
```

#### Step-3: Run Update and Install

```sh
sudo apt-get update
sudo apt-get install nodejs -y
```

### 0.1.7 Install npm

```shell
sudo apt install -y npm
npm -v
sudo npm install npm -g
```

### 0.1.8 Install expo SDK

```shell
npx expo install
```

## 0.2 U2D2 Configuration

### 0.2.1 Connect U2D2 to Raspberry Pi

### 0.2.2 Configure the latency

```shell
cat /sys/bus/usb-serial/devicees/ttyUSB0/latency_timer
16
echo 1 > /sys/bus/usb-serial/devices/ttyUSB0/latency_timer
cat /sys/bus/usb-serial/devices/ttyUSB0/latency_timer
1
```

## USING EAS INSTEAD OF EXPO

using eas instead of expo since expo is deprecated.

### Install eas-cli

```sh
sudo npm install -g eas-cli
```

### Start eas-cli

```sh
npx eas-cli
```





# 1 Build

## 1.1 APP Build and Publish

### 1.1.1 Expo Login

```shell
npx expo login
```

Input the user name and password when they're required.



### 1.1.1 IOS

1. Download Expo App.

2. Create an Expo account

3. Publish the APP

   ```she
   cd ./BlossomApp
   expo publish
   ```
