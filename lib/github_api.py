import requests


class GithubAPI:

    @classmethod
    def get_browser_download_url_latest_release(cls):
        try:
            response = requests.get("https://api.github.com/repos/omides248/iran_dns/releases/latest", timeout=1)
            tag_name = response.json()["tag_name"]
            browser_download_url = response.json()["assets"][0]["browser_download_url"]
            filename = response.json()["assets"][0]["name"]
            return tag_name, browser_download_url, filename
        except Exception as e:
            print(e)
            return "", "", ""
