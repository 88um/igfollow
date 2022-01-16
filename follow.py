import os, time
try:
    import stdiomask
    from InstagramAPI import InstagramAPI
    from random import randint
except:
    os.system('pip install InstagramAPI')
    os.system('pip install random')
    os.system('pip install stdiomask')
    import stdiomask
    from InstagramAPI import InstagramAPI
    from random import randint

FromFollowingList = False
FromFollowerList = False

banner = ("""
  ____  __ __  ______   ___          _____   ___   _      _       ___   __    __ 
 /    ||  |  ||      | /   \        |     | /   \ | |    | |     /   \ |  |__|  |
|  o  ||  |  ||      ||     | _____ |   __||     || |    | |    |     ||  |  |  |
|     ||  |  ||_|  |_||  O  ||     ||  |_  |  O  || |___ | |___ |  O  ||  |  |  |
|  _  ||  :  |  |  |  |     ||_____||   _] |     ||     ||     ||     ||  `  '  |
|  |  ||     |  |  |  |     |       |  |   |     ||     ||     ||     | \      / 
|__|__| \__,_|  |__|   \___/        |__|    \___/ |_____||_____| \___/   \_/\_/  
                                                                                 
  
                    ~By @Crackled on tele.~
""")



def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(banner)


def login():
    global ig, nam, self_id
    while True:
        clear()
        nam = input('[+] Username: ')
        pas = stdiomask.getpass('[+] Password: ')
        ig = InstagramAPI(nam, pas)
        success = ig.login()
        if not success:
            time.sleep(6)
        else:
            ig.getSelfUsernameInfo()
            self_id = ig.LastJson['user']['pk']
            break
    main()
    


def main():
    global  fol, speed , myfolowing, FromFollowerList, FromFollowingList, targ
    while True:
                
                myfolowing = GetAllFollowing(self_id)
                clear()
                print(f'[-] Logged in user: {nam}\n')
                target = (input('[1] Follow targets from following list\n[2] Follow targets from follower list\n[3] Follow targets from external list\n\n[+] Choose One:  '))
                if target == '1':
                    targ = input('[+] Target user: ')
                    FromFollowingList = True
                elif target == '2':
                    targ = input('[+] Target user: ')
                    FromFollowerList = True
                fol = int(input('[+] How many people to follow: '))
                clear()
                speed = input("""[-] Determine your follow speed\n\n[1] Fast 10-15 sec delay
[2] Medium 20-30 sec delay
[3] Slow 45-90 sec delay\n\n[+] Choose One: """)
                if speed == '1':
                    speed = randint(10,15)
                    Follow()
                elif speed == '2':
                    speed = randint(20,30)
                    Follow()
                elif speed == '3':
                    speed = randint(45,90)
                    Follow()
                else:
                    pass


def GetAllFollowing(user_id):
    following = []
    next_max_id = True
    while next_max_id:
        if next_max_id is True:
            next_max_id = ''
        _ = ig.getUserFollowings(user_id, maxid=next_max_id)
        following.extend(ig.LastJson.get('users', []))
        next_max_id = ig.LastJson.get('next_max_id', '')
    following = set([_['pk'] for _ in following])
    return following


def GetAllFollowers(user_id):
    followers = []
    next_max_id = True
    while next_max_id:
        if next_max_id is True:
            next_max_id = ''
        _ = ig.getUserFollowers(user_id, maxid=next_max_id)
        followers.extend(ig.LastJson.get('users', []))
        next_max_id = ig.LastJson.get('next_max_id', '')
    followers = set([_['pk'] for _ in followers])
    return followers


def convert(file):
    converted = []
    for line in file:
        try:
            ig.searchUsername(line)
            id = ig.LastJson['user']['pk']
            if id not in myfolowing:
                if id not in converted:
                    converted.append(id)
        except:
            continue
    return converted


def Follow():
    done = 0
    error = 0
    err = 0
    if FromFollowerList:
        ig.searchUsername(targ)
        try:
            user_id = ig.LastJson['user']['pk']
            following = GetAllFollowers(user_id)
            if len(following) < fol:
                foll = len(following)
            elif len(following) == 0:
                print('[NONE] No new target users found.')
                time.sleep(5)
                return
            else:
                foll = fol
        except:
            print(f'[ERROR] Could not find user {targ}' )
            time.sleep(5)
            return
    
    elif FromFollowingList:
        ig.searchUsername(targ)
        try:
            user_id = ig.LastJson['user']['pk']
            following = GetAllFollowing(user_id)
            if len(following) < fol:
                foll = len(following)
            elif len(following) == 0:
                print('[NONE] No new target users found.')
                time.sleep(5)
                return
            else:
                foll = fol
        except:
            print(f'[ERROR] Could not find user {targ}' )
            time.sleep(5)
            return
    else:
        try:
            file = open('followlist.txt', 'r').read().splitlines()
        except:
            print("[!] Set your target list in 'followlist.txt' first!")
            with open('followlist.txt', 'a') as f:
                f.write(f'pubity\night')
            time.sleep(5)
            return
        following = convert(file)
        if len(following) < fol:
            foll = len(following)
        elif len(following) == 0:
            print('[NONE] No new target users found.')
            time.sleep(5)
            return
        else:
            foll = fol
    print('\n[+] Following {}/{} users'.format(foll, len(following)))
    time.sleep(3)
    for usr in following:
        try:
            ig.getUsernameInfo(str(usr))
            user = ig.LastJson['user']['username']
            ig.follow(str(usr))
            done+=1
            clear()
            print(f"[-] Done: {done} | Errors: {err} | Last Followed: {user}")
            if done == foll:
                break
            else:
                time.sleep(speed)
        except KeyboardInterrupt:
            return
        except:
            err+=1
            error+=1
            print('\n[!] First Error in following (maybe soft block)...sleep 15 min')
            if error == 3:
                print('[!] 3x Error in following...sleep one hour')
                time.sleep(3601)
                error = 0
            else:
                time.sleep(901)
    
    print('\n[DONE] Followed all users! Returning to main function. ')
    time.sleep(9)
    
        

if __name__ == "__main__":
    login()