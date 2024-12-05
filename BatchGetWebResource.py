# pip install requests
# pip install bs4

import requests
from bs4 import BeautifulSoup
import urllib.parse
import os

def find_resources(url):
    try:
        # 获取网页内容
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功

        # 解析HTML内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 提取资源文件URL的集合
        resources = set()

        # 提取<img>标签的src属性
        for img in soup.find_all('img'):
            src = img.get('src')
            if src:
                resources.add(urllib.parse.urljoin(url, src))

        # 提取<link>标签的href属性（通常是CSS文件）
        for link in soup.find_all('link', rel=True):
            if any(rel_value.lower() in ['stylesheet', 'icon'] for rel_value in link['rel']):
                href = link.get('href')
                if href:
                    resources.add(urllib.parse.urljoin(url, href))
        href = link.get('href')
        if href:
            resources.add(urllib.parse.urljoin(url, href))

        # 提取<script>标签的src属性
        for script in soup.find_all('script'):
            src = script.get('src')
            if src:
                resources.add(urllib.parse.urljoin(url, src))

        # 提取<a>标签的href属性
        for a in soup.find_all('a'):
            href = a.get('href')
            if href:
                resources.add(urllib.parse.urljoin(url, href))

        return resources

    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return set()

def download_file(url, local_folder):
    try:
        # 发送HTTP GET请求获取文件
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 检查请求是否成功
 
        # 从URL中提取文件名
        filename = os.path.basename(urllib.parse.urlparse(url).path)
 
        # 检查文件扩展名
        if filename.lower().endswith(('.pdf', '.step', '.zip','.rar')):
            # 构建本地文件路径
            local_file_path = os.path.join(local_folder, filename)
 
            # 以二进制模式打开本地文件准备写入
            with open(local_file_path, 'wb') as f:
                # 从响应中逐块读取文件内容并写入本地文件
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
 
            print(f"Downloaded {filename} to {local_file_path}")
        else:
            print(f"Skipped {filename} (unneeded file)")
 
    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")
 
def main():
    url = 'https://www.aubo-robotics.cn/download'  # 替换为你要检查的URL
    local_folder = r"D:\仪器说明书\遨博机械臂"        # 替换为你的本地文件夹路径
 
    # 确保本地文件夹存在
    os.makedirs(local_folder, exist_ok=True)
 
    resources = find_resources(url)

    # 打印找到的资源文件
    for resource in resources:
        print(resource)
 
    # 遍历资源并下载符合条件的文件
    for resource in resources:
        download_file(resource, local_folder)

if __name__ == "__main__":
    main()