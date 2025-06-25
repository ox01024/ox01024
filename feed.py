import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime



def fetch_feed(rss_url, feed_size):
    """Fetch and print the RSS feed from the specified URL."""
    req = urllib.request.Request(rss_url, headers={"User-Agent": "Mozilla/5.0"})
    response = urllib.request.urlopen(req).read().decode("utf-8")
    root = ET.fromstring(response)
    items = root.findall(".//item")
    feed_info = ''
    for item in items[:feed_size]:
        title = item.find("title")
        link = item.find("link")
        time = item.find("pubDate")
        time = parsedate_to_datetime(time.text)
        time = time.astimezone(timezone(timedelta(hours=8)))
        time = time.strftime("%Y-%m-%d %H:%M:%S")
        feed_info += f"- [{title.text}]({link.text}) {time}\n"
    return feed_info

def fetch_list_of_readme(flag):
    """Fetch the list of README files from the repository."""
    with open("README.md", "r") as f:
        readme_content = f.read()
        if flag == "blog":
            start_marker = "<!-- blog starts -->\n"
            end_marker = "\n<!-- blog ends -->"
        elif flag == "podcast":
            start_marker = "<!-- podcast starts -->\n"
            end_marker = "\n<!-- podcast ends -->"
        matches = re.findall(f"{start_marker}(.*?){end_marker}", readme_content, re.DOTALL)
        if not matches:
            return None
    return matches[0]

def replace_readme_content(old_info, new_info):
    """Replace the old_info with new_info in the README.md file."""
    with open("README.md", "r+") as f:
        readme_content = f.read()
        readme_content = readme_content.replace(old_info, new_info)
        f.seek(0)
        f.truncate(0)
        f.write(readme_content)


if __name__ == "__main__":
    blog_rss_url = "https://not-only-security.pages.dev/index.xml"
    podcast_rss_url = "https://feed.xyzfm.space/rrenlp6dvhtv"
    feed_size = 5
    blog_feed_info = fetch_feed(blog_rss_url, feed_size)
    podcast_feed_info = fetch_feed(podcast_rss_url, feed_size)
    
    old_blog_feed_info = fetch_list_of_readme("blog")
    old_podcast_feed_info = fetch_list_of_readme("podcast")
    
    if old_blog_feed_info != blog_feed_info:
        print(old_blog_feed_info, blog_feed_info)
        replace_readme_content(old_blog_feed_info, blog_feed_info)
        print("Blog feed updated in README.md")
    
    if old_podcast_feed_info != podcast_feed_info:
        replace_readme_content(old_podcast_feed_info, podcast_feed_info)
        print("Podcast feed updated in README.md")