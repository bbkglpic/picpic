import os
import re
import requests

def download(filename):
    content = ""
    with open(filename) as f:
        content = f.read()
    pat = r"!\[(.*)\]\((.*)\)"
    matchlist = re.findall(pat, content)
    # print(matchlist)
    imglist = []
    for img in matchlist:
        url = img[1]
        imgname = str(url).split('/')[-1]
        imglist.append(imgname)
        r = requests.get(url)
        if (r.status_code == 200):
            with open("img/" + imgname, "wb") as f:
                f.write(r.content)

    old2newline = []
    for imgname in imglist:
        newurl = "https://raw.githubusercontent.com/bbkglpic/picpic/master/img/" + imgname
        oldline = None
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                if imgname in line:
                    oldline = line
                    break
        if oldline:
            newline = ""
            for ch in oldline:
                if ch == ' ':
                    newline += ch
                else:
                    break
            newline += "![{}]({})".format(imgname.split(".")[0], newurl)
            if (oldline[-1] == '\n'):
                oldline = oldline[0:-1]
            old2newline.append([oldline, newline])
    # print(old2newline)
    with open(filename) as f:
        content = f.read()
        for l2l in old2newline:
            content = content.replace(l2l[0], l2l[1])

    print(content)
    with open(filename, 'w') as f:
        f.write(content)



if __name__ == "__main__":
    dir = "/home/bbkgl/mymd/bbkgl.github.io/_posts/"
    filelist = os.listdir(dir)
    for file in filelist:
        if file < "2019-11-07-面向对象系统分析与设计":
            print(file)
            try:
                download(dir + file)
            except:
                print(file)
                continue
