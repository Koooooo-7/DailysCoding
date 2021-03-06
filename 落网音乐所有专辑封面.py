import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool



# 解析当前页面
def get_page(current_url):
    headers = {
        "User - Agent": "Mozilla / 5.0(Windows NT 6.1;Win64;x64) AppleWe\
        bKit / 537.36(KHTML, likeGecko) Chrome / 67.0.3396.87Safari / 537.36"
    }
    res = requests.get(current_url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    # 获取页面10张图片地址
    img_urls = soup.find_all('img', class_='cover rounded')
    return img_urls


# 获取图片链接
def get_src(img_urls):
    images = []
    for img in img_urls:
        images.append(img['src'])
    return images


def download_img(images, num):
    x = num*10
    y = 0
    for image in images:
        html = requests.get(image)
        name = str(x+y)
        print(name)
        with open(name+'.jpg', 'wb') as f:
            f.write(html.content)
        y += 1


def run(current_url, num):
    urls = get_page(current_url)
    images = get_src(urls)
    download_img(images, num)


if __name__ == '__main__':
    const_url = "http://www.luoo.net/tag/?p="
    pool = Pool(5)
    for i in range(1, 100):
        now_url = const_url+str(i)
        pool.apply_async(run(now_url, i), args=(i,))
    pool.close()
    pool.join()

