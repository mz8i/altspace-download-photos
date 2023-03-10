# Download all your photos from AltspaceVR


## Set up

1. Download latest [Python](https://www.python.org/downloads/)
2. Install dependencies of the project by running `pip install requests bs4` in the command line of your operating system

## Running

1. Log in onto to AltspaceVR website
2. Go to https://account.altvr.com/photos/
3. Look at the URL. It should now look like `https://account.altvr.com/photos/share?token=SOMERANDOMCHARACTERS`
4. Copy the characters of the token
5. In the project directory, run `python run.py --token TOKEN_HERE --download images` where you should replace `TOKEN_HERE` with the characters taken from the URL
6. The program will run and save all your photos to the `images` subfolder of the same folder where you downloaded the `run.py`