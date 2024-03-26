from src.get import *
from src.util import *  
import time
import threading
import base64

def avatar_changer():
    cmd.rst() 
    print(f"{cc.m}Put a .png image inside of data with the name avatar.png if u want a custom one")
    for token in gt.tokens():
        t = threading.Thread(target=change_avatar, args=(token,))
        t.start()
        t.join()

def change_avatar(token, silient=False, code=False):
    session = gt.ss()
    with open("data/avatar.png", "r") as f:
        avatar = f.read()
    try:
        r = session.patch(
            "https://discord.com/api/v9/users/@me",
            headers=headers(token),
            json={"avatar": f"data:image/png;base64,{(base64.b64encode(avatar).decode('utf-8'))}"},
        )

        status = r.status_code
        text = r.text

        debug(status, text)

        if not silient:
            if status == 200:
                log.cus.g(status, text, token, "Changed")
            elif status == 429:
                log.r(status, text, token)
                text = json.loads(text)
                slip = float(text.get('retry_after'))
                time.sleep(slip)
            elif status == 401:
                log.i(status, text, token)
            else:   
                log.un(status, text, token)

        
    except Exception as e:
        debug(e)
        
