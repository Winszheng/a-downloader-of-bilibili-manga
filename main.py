import requests
import os

URL_IMAGE = "https://manga.hdslb.com/bfs/manga/"
URL_IMAGE_TOKEN = "https://manga.bilibili.com/twirp/comic.v1.Comic/ImageToken?device=pc&platform=web"
URL_IMAGE_ALL = "https://manga.bilibili.com/twirp/comic.v1.Comic/GetImageIndex?device=pc&platform=web"
URL_DETAIL = "https://manga.bilibili.com/twirp/comic.v2.Comic/ComicDetail?device=pc&platform=we"

# COOKIES = {{你的cookie}}
cookies = requests.cookies.RequestsCookieJar()
# for c in COOKIES.split(";"):
#     key, value = c.split("=")
#     cookies.set(key, value)

def download_chapter(ch_num, mc_name = "default", ch_name = "default"):
    dir_name = "manga/"+mc_name+"/"+ch_name+"/"
    os.makedirs(dir_name)
    images = requests.post(URL_IMAGE_ALL, cookies = cookies, data = {"ep_id":ch_num}).json()['data']['images']
    index = 1
    for i in images:
        img_url = i['path']
        data = {"urls": "[\""+img_url+"@1100w.jpg\"]"}
        r = requests.post(URL_IMAGE_TOKEN, data = data).json()
        get_image_url = r['data'][0]['url'] + '?token=' + r['data'][0]['token']
        r = requests.get(get_image_url, stream=True)
        name = str(index)+".jpg"
        with open(dir_name+name, 'wb') as fd:    # wb表字节写入
            for chunk in r.iter_content():
                fd.write(chunk)
        index = index+1
    print(ch_name+" 下载完毕")

def download_all(mc_num):
    r = requests.post(URL_DETAIL, data = {"comic_id": mc_num}).json()['data']
    mc_name = r['title']
    r = r['ep_list']
    for i in r:
        ch_num = i['id']
        ch_name = i['short_title']+' '+i['title']
        download_chapter(ch_num, mc_name = mc_name, ch_name = ch_name)

    print("下载至最新")

# 主程序入口
mc_num = input("请输入作品的mc号: ")
print("1.下载至最新")
print("2.下载单章")
print("输入其他任意键退出")
flag = input()

if not(os.path.exists("manga")):
    os.mkdir("manga")

if flag == "1":
    download_all(mc_num)
    pass
elif flag == "2":
    ch_num = input("请输入章节号: ")
    download_chapter(ch_num)
else:
    exit(0)
