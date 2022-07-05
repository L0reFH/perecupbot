import vk
import json
import requests 

session = vk.UserAPI(user_password="odKpY71I", user_login=89952736214, scope="wall, photos", v="5.131")

up_url = session.photos.getWallUploadServer()["upload_url"]

with open("./123.jpg", "rb") as f:
    resp = requests.post(f"{up_url}", files={"file": f})
    print(resp.json())
    saveWallPhoto = session.photos.saveWallPhoto(server=resp.json()["server"], photo=resp.json()["photo"], hash=resp.json()["hash"])
    attachments = []
    attachments.append("photo{}_{}".format(saveWallPhoto[0]["owner_id"], saveWallPhoto[0]["id"]))
    session.wall.post(attachments=attachments)