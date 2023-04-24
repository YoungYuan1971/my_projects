import requests
from faker import Faker

fake = Faker()
headers = {'user-agent': fake.chrome()}


def request_html(url):
    response = requests.get(url, headers=headers)
    return response


def main():
    domain = input("请输入域名：").strip()
    base_url = f"https://www.google.com/s2/favicons?sz=64&domain={domain}"
    ico = request_html(base_url).content

    with open(f'网站图标/{"_".join(domain.split(".")[:-1])}.png', 'wb') as f:
        f.write(ico)
        print("下载成功!")


if __name__ == "__main__":
    main()
