# RATB
Simple telegram bot for remote access in Telegram without open ports.

![Banner](banner.png)

# How to run
## For self-assembly
1. Install **requirements.txt**.
2. Change in **config file** `bot_token` variable to your token from BotFather.
3. Change in **config file** `bot_users` array to allowed users or user.
4. If you want to collect logs, then set the `write_logs` parameter to 1.
5. Open **cam.py** (or compile into an *.exe* via **auto-py-to-exe** module).
## For a binary releases
1. Change in **configs/default.json** `bot_token` variable to your token from BotFather.
2. Change in **configs/default.json** `bot_users` array to allowed users or user.
3. If you want to collect logs, then set the `write_logs` parameter to 1.
4. Open **cam.exe**.

# Configuration
```
{
    "bot_token": "",
    "bot_users": [],
    "write_logs": 0,
    "file_logs": "logs.log",
    "mode_logs": "w",
    "format_logs": "%(asctime)s %(levelname)s %(message)s"
}
```

# How to use
**There are inline buttons here.**
Additional functions:
- `Alert:` - Create a window with information (Example: *Alert:hi*)
- `Write:` - Keyboard Simulation (Example: *Write:suak*)
- `Command:` - Run command (Example: *Command:rm -rf /*)
