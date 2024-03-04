import os
import sys
import requests
import time
import asyncio
import aiohttp
import aiofiles
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor


def download_images_from_url(url):
    try:
        start_time = time.time()
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            img_tags = soup.find_all('img')
            image_urls = [urljoin(url, img_tag.get('src')) for img_tag in img_tags if img_tag.get('src')]
            # Using ThreadPoolExecutor to download images asynchronously
            with ThreadPoolExecutor(max_workers=5) as executor:
                executor.map(download_image, image_urls)
        else:
            print(f'Failed to fetch {url}. Status code: {response.status_code}')
        print(f'Downloading images from {url} took {time.time() - start_time:.2f} seconds')
    except Exception as e:
        print(f'Error fetching {url}: {str(e)}')


async def async_download_image(session, url):
    try:
        start_time = time.time()
        async with session.get(url) as response:
            if response.status == 200:
                filename = os.path.basename(urlparse(url).path)
                image_path = os.path.join("image_parser", filename)
                async with aiofiles.open(image_path, 'wb') as f:
                    await f.write(await response.read())
                print(f'Downloaded {filename} in {time.time() - start_time:.2f} seconds')
            else:
                print(f'Failed to download {url}. Status code: {response.status}')
    except Exception as e:
        print(f'Error downloading {url}: {str(e)}')


async def async_download_images_from_url(url):
    try:
        async with aiohttp.ClientSession() as session:
            start_time = time.time()
            async with session.get(url) as response:
                if response.status == 200:
                    soup = BeautifulSoup(await response.text(), 'html.parser')
                    img_tags = soup.find_all('img')
                    image_urls = [urljoin(url, img_tag.get('src')) for img_tag in img_tags if img_tag.get('src')]
                    await asyncio.gather(*[async_download_image(session, img_url) for img_url in image_urls])
                else:
                    print(f'Failed to fetch {url}. Status code: {response.status}')
                print(f'Downloading images from {url} took {time.time() - start_time:.2f} seconds')
    except Exception as e:
        print(f'Error fetching {url}: {str(e)}')


def download_image(url):
    try:
        start_time = time.time()
        response = requests.get(url)
        if response.status_code == 200:
            filename = os.path.basename(urlparse(url).path)
            image_path = os.path.join("image_parser", filename)
            with open(image_path, 'wb') as f:
                f.write(response.content)
            print(f'Downloaded {filename} in {time.time() - start_time:.2f} seconds')
        else:
            print(f'Failed to download {url}. Status code: {response.status_code}')
    except Exception as e:
        print(f'Error downloading {url}: {str(e)}')


async def main_async(urls):
    await asyncio.gather(*[async_download_images_from_url(url) for url in urls])


def main_sync(urls):
    pool = Pool(processes=5)
    pool.map(download_images_from_url, urls)
    pool.close()
    pool.join()


def main_multiprocess(urls):
    with Pool(processes=5) as pool:
        pool.map(download_images_from_url, urls)


if __name__ == "__main__":
    # Проверяем, были ли предоставлены аргументы командной строки
    if len(sys.argv) > 1:
        urls = sys.argv[1:]
    else:
        # Если аргументы не были предоставлены, запрашиваем ввод у пользователя
        urls = ['https://k3d.tech/vostok/']
    # Если список URL-адресов пуст, выводим сообщение и завершаем программу
    if not urls:
        print("No URLs provided.")
        sys.exit()

    start_total_time = time.time()

    # Выполняем синхронное выполнение
    print('Start synchronous execution')
    main_sync(urls)
    print(f'End: total time taken: {time.time() - start_total_time:.2f} seconds')

    # Выполняем асинхронное выполнение
    print('Start asynchronous execution')
    asyncio.run(main_async(urls))
    print(f'End: total time taken: {time.time() - start_total_time:.2f} seconds')

    # Выполняем многопроцессорное выполнение
    print('Start multiprocess execution')
    main_multiprocess(urls)
    print(f'End: total time taken: {time.time() - start_total_time:.2f} seconds')
