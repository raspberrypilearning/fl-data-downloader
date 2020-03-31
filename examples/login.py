from fl_data_downloader import login, store_credentials

# login and get a browser context, you will be prompted to enter a username 
# and password
b = login()

# login with a specific username and password
b = login(["user", "password"])

# store credentials to be used each time login() is called, you will be 
# prompted to enter a username and password

# the login configuration data is stored in `~/.fl-data-dl` (Linux, macOS) or 
# `%USERPROFILE%\.fl-data-dl` (Windows) in plain text. If you are not confident 
# your computer is secure you should not use this option.
store_credentials()