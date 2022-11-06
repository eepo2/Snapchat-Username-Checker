import httpx, ctypes, os, pyfiglet, sys, time; from itertools import cycle


class bcolors:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


class GetUsername:
    def Getuser():
        with open('Data/usernames.txt', 'r') as temp_file:
            usernames = [line.rstrip('\n') for line in temp_file]
        return usernames
    username = Getuser()
    username_pool = cycle(username)


class ClipChecker:
    def __init__(self):
        self.set_title()
        self.logo()


    def set_title(self):
        if os.name == 'nt':
            ctypes.windll.kernel32.SetConsoleTitleW(f"ClipChecker | clipssender#2940 | discord.gg/snapify | https://discord.gg/clipssender")
        else:
            ctypes.windll.kernel32.SetConsoleTitleW(f"ClipChecker | clipssender#2940 | discord.gg/snapify | https://discord.gg/clipssender")

    def logo(self):
        os.system('cls')
        print(pyfiglet.figlet_format(f"SnapChecker"))
        print(f"{bcolors.RED}Author: clipssender#2920{bcolors.RESET}")

    def checker(self):
        try:
            username = next(GetUsername.username_pool)
    
            client=httpx.Client(
    
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36", 
                    'Accept-Encoding':'gzip'},
                timeout=30
                ) 
    
            client.get('https://accounts.snapchat.com/accounts/login') # make request to get xsrf token in cookies
            xsrf_token = client.cookies['xsrf_token'] # get xsrf token from cookies
    
            self.res=client.post('https://accounts.snapchat.com/accounts/get_username_suggestions', data={
                    "requested_username": username,
                    "xsrf_token": xsrf_token
                }) 
            
            if self.res.text=="":
                print(f'{bcolors.RED}Ratelimited, waiting for {bcolors.GREEN}30{bcolors.RESET}{bcolors.RED} seconds before continueing{bcolors.RESET}')
                time.sleep(30)
                client.get('https://accounts.snapchat.com/accounts/login')
                xsrf_token = client.cookies['xsrf_token']
            else:
                pass


            if self.res.json()['reference']['status_code'] == 'OK':

                print(f'{bcolors.GREEN}Username is Available: {username}{bcolors.RESET}')
                with open('out/checked_usernames.txt','a') as f:
                    f.write(f'{username}\n')


            elif self.res.status_code==429:
                print(f'{bcolors.RED}Ratelimited: {username}{bcolors.RESET}') 
                time.sleep(10)

            elif self.res.json()['reference']['status_code'] == 'TAKEN':
                print(f'{bcolors.RED}Username is Taken: {username}{bcolors.RESET}')

            else:
                print(f'{bcolors.RED}Error: {self.res.text} | Status Code: {self.res.status_code}{bcolors.RESET}')

        except:
            pass
    
    def main(self):
        for i in range(int(len(open('Data/usernames.txt', 'r').read().splitlines()))):
            self.checker()
        print(f'{bcolors.GREEN}Finished Checking All usernames{bcolors.RESET}')
        input('Press Enter to Exit')
        sys.exit()


if __name__=="__main__":
    try:
        ClipChecker().main()
    except KeyboardInterrupt:
        sys.exit()




    
    
