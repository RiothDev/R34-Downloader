import os, requests, io, re, threading, colorama
from bs4 import BeautifulSoup
from PIL import Image

class Request:
    def __init__(self, tags: str) -> None:
        self.url = "https://rule34.paheal.net/post/list/{}/".format(tags)
    
    def get_images(self, page: int) -> list:
        response = requests.get(url=self.url + str(page)).text
        soup = BeautifulSoup(response, "lxml")

        content = soup.find_all("a", {"class": "shm-thumb-link"})

        urls = []
        images = []

        for x in content:
            url = "https://rule34.paheal.net{0}#search={1}".format(str(x["href"]), self.url.split("/")[5])
            urls.append(url)
        
        for x in urls:
            try:
                img_request = requests.get(url=x).text
                img_soup = BeautifulSoup(img_request, "lxml")

                image_url = str(img_soup.find("img", {"class": "shm-main-image"})["src"])
                images.append(image_url)

            except Exception as err:
                pass

        return images
    
    def download(self, img: str, path: str) -> None:
        try:
            ext = "." + re.search(r"\.([a-zA-Z0-9]+)$", img).group(1)

            response = requests.get(img).content
            image = Image.open(io.BytesIO(response))

            index = str(len(os.listdir(path=path)) + 1)

            image.save(os.path.join(path, "image" + index) + ext)
            print(colorama.Fore.YELLOW + "- Image {0} downloaded".format(index))
        
        except Exception as err:
            pass
    
    def download_images(self, images: list) -> None:
        path = os.path.join(os.getcwd(), "r34")

        if not os.path.exists(path=path):
            os.mkdir(path=path)
        
        threads = []

        for img in images:
            thread = threading.Thread(target=self.download, args=(img, path,))
            threads.append(thread)
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()

def main():
    colorama.init()

    def send_request(data: tuple) -> None:
        request = Request(tags=data[0])
        images = request.get_images(page=data[1])

        request.download_images(images=images)

    def init() -> None:
        os.system("cls")

        try:
            tags = str(input(colorama.Fore.BLUE + "> Tags: " + colorama.Fore.CYAN))
            tags = "%20".join(x for x in tags.split(" "))

            pages = int(input(colorama.Fore.BLUE + "> Pages: " + colorama.Fore.CYAN))
            threads = []

            print(colorama.Fore.YELLOW + "\n--- Downloading images...")

            for i in range(pages):
                thread = threading.Thread(target=send_request, args=((tags, i + 1),))
                threads.append(thread)
            
            for thread in threads:
                thread.start()
            
            for thread in threads:
                thread.join()
            
            init()

        except Exception as err:
            print(colorama.Fore.RED + "> Error trying to perform the task" + colorama.Fore.RESET)
            init()

    init()

if __name__ == "__main__":
    main()