# Guide to Set Up a Raspberry Pi Zero 2 W to Host a Discord Bot

## 1. Prepare the Raspberry Pi Zero 2 W

### Install Raspberry Pi OS:

1. Download Raspberry Pi Imager from the [official Raspberry Pi website](https://www.raspberrypi.org/software/).
2. Insert your microSD card into your computer and run Raspberry Pi Imager.
3. Select **Raspberry Pi OS (32-bit)** as the operating system.
4. Click the gear icon to configure:
   - Enable **SSH** (recommended for headless setup).
   - Set the hostname (e.g., `raspberrypi`).
   - Enter your Wi-Fi credentials to automatically connect the Pi to the internet.
   - Set a password for SSH login.
5. Write the image to the microSD card, then insert it into the Raspberry Pi and power it on.

### Connect via SSH:

If you're using the Pi headless (without a monitor/keyboard):

1. SSH into your Pi:
   ```bash
   ssh <username>@raspberrypi.local
   ```
  -Replace <username> with the username set during the Raspberry Pi Imager setup.

## 2. Update and Install Python

Update your Raspberry Pi OS packages:

```bash
sudo apt update
sudo apt upgrade -y
```

Check Python 3 installation:
```bash
python3 --version
```

If Python 3 isn’t installed, install it:

```bash
sudo apt install python3 python3-pip
```

## 3. Install discord.py and Set Up a Virtual Environment
Why Use a Virtual Environment?
Installing Python packages globally can cause conflicts with system packages, so it’s better to isolate the environment using a virtual environment.

Install required packages for virtual environments:
```bash
sudo apt install python3-venv python3-pip
```
Create a virtual environment:
Navigate to your bot directory or any desired folder, then run:

```bash
python3 -m venv bot-env
```
This will create a virtual environment named `bot-env`.

Activate the virtual environment:
```bash
source bot-env/bin/activate
```

The terminal prompt should change, indicating that the virtual environment is active.

Install discord.py inside the virtual environment:
With the virtual environment active, install discord.py:

## 4. Clone Your Discord Bot Repository
Install Git (if not installed):
```bash
sudo apt install git
```

Clone your GitHub repository:
```bash
git clone https://github.com/Tide44-cmd/CabinSquadBot.git
```
Navigate to the bot’s directory:
```bash
cd CabinSquadBot
```

Configure your bot:
Open the `main.py` file to set your bot’s Discord token:
```bash
nano main.py
```

Replace the placeholder token with your actual Discord bot token in the following line:

```bash
bot.run('YOUR_DISCORD_BOT_TOKEN')
```
Save and exit (Ctrl + X, then Y and Enter).

## 5. Run the Discord Bot
Activate the virtual environment (if not already activated):
```bash
source bot-env/bin/activate
```
Run the bot:
```bash
python3 main.py
```

At this point, the bot should connect to Discord and respond to commands.

## 6. Set Up Auto-Start for the Discord Bot (with Virtual Environment)
To ensure your bot starts automatically when the Raspberry Pi boots, we can use systemd. Since you’re using a virtual environment, we need to activate the environment before starting the bot.

Create a systemd service file:
```bash
sudo nano /etc/systemd/system/discordbot.service
```
Add the following configuration to the service file:
```bash
[Unit]
Description=Discord Bot Service
After=network.target

[Service]
User=<username>
WorkingDirectory=/home/<username>/CabinSquadBot
ExecStart=/home/<username>/bot-env/bin/python /home/<username>/CabinSquadBot/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```
  - User: Set to the user you’re logged in as (e.g., `pi`). 
  
  - WorkingDirectory: The directory where your bot is located (`/home/pi/CabinSquadBot`).  
  
  - ExecStart: The path to the Python executable inside your virtual environment (`/home/pi/bot-env/bin/python`), followed by the path to your bot’s `main.py`.

### Enable and start the service:
Enable the service to start on boot:
```bash
sudo systemctl enable discordbot
```
Start the service immediately:
```bash
sudo systemctl start discordbot
```
Check the service status:
To ensure that the bot is running:
```bash
sudo systemctl status discordbot
```
This should show that the bot is active and running.

*If you have an error here check the directories are correct in your `discordbot` service file*

*Verify the Working Directory:*
*Use the `pwd` command to confirm that your current directory matches the path you have set.*
*Check the Python Directory:*
*While inside your virtual environment, use the `which python` command to ensure it points to the correct Python executable.*



## Conclusion
With these steps, you’ve set up a Raspberry Pi Zero 2 W to host your Discord bot, ensured it runs in a virtual environment, and configured it to start automatically on boot. If you ever update your bot or need to pull changes from your GitHub repository, remember to restart the service.

To stop and restart the bot service manually:

Stop the bot:

```bash
sudo systemctl stop discordbot
```
Restart the bot:

```bash
sudo systemctl restart discordbot
```



