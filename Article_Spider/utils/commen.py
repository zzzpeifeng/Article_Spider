import hashlib


def get_md5(url):
    if isinstance(url,str):
        url=url.encode('utf-8')
    m=hashlib.md5()
    m.update(url)
    return m.hexdigest()

if __name__ == "__main__":
    str='http://blog.jobbole.com/all-posts/'
    print(get_md5(str.encode('utf-8')))