
import requests, re, urlparse


target_url = "website/ip"
target_links = []


def extract_links(url):
    response = requests.get(url)
    href_links = re.findall('(?:href=")(.*?)"', response.content)
    href_links_2 = re.findall("(?:href=')(.*?)'", response.content)
    return href_links + href_links_2


def crawl(url):
    href_links = extract_links(url)
    for link in href_links:
        link = urlparse.urljoin(url, link)

        if "#" in link:
            link = link.split("#")[0]

        if target_url in link and link not in target_links:
            target_links.append(link)
            print(link)
            crawl(link)


crawl(target_url)