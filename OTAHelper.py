from selectolax.lexbor import LexborHTMLParser
from http.cookies import BaseCookie
from asyncio import sleep, create_task
from dataclasses import dataclass
from aiohttp import ClientSession
from typing import Optional
from re import compile

from os import listdir, path, removedirs, mkdir


regexPattern = compile(
    r"(\d+\.\d+\.\d+)\s\((\w+\.\w+\.\w+)(\.[^,]+)?,\s(\w+\s\w+)(,\s.+)?\)"
)


@dataclass
class OTAInfo:
    androidVersion: str
    buildVersion: str
    subVersion: Optional[str]
    releaseDate: str
    user: Optional[str]
    downloadLink: str


class OTAChecker:
    def __init__(self) -> None:
        self.preferDict: dict[str, OTAInfo] = {}

    async def updateOTAInfo(self):
        async with ClientSession() as s:
            s.cookie_jar.update_cookies(
                BaseCookie({"devsite_wall_acks": "nexus-ota-tos"})
            )
            res = await s.get("https://developers.google.com/android/ota")
            soup = LexborHTMLParser(await res.text())
            targets = soup.css('tr[id^="husky"]')
            if len(targets) == 0:
                print("error")
                return
            for target in targets:
                version = target.css_first("td")
                if not version:
                    print("error: version not found.")
                    continue
                versionText = version.text()
                match = regexPattern.match(versionText)
                if not match:
                    print("error: match failed.")
                    continue
                downloadLink = target.css_first("a")
                if not downloadLink:
                    print("error: download link not found.")
                    continue
                result = [*match.groups(), downloadLink.attributes["href"]]
                info = OTAInfo(*result)
                if info.releaseDate in self.preferDict:
                    continue
                if info.user is None:
                    self.preferDict[info.releaseDate] = info
                elif "TW" in info.user:
                    self.preferDict[info.releaseDate] = info

        await sleep(86400)
        create_task(self.updateOTAInfo())

    async def download(self, url: str, filename: str):
        async with ClientSession() as s:
            async with s.get(url) as res:
                with open(filename, "wb") as f:
                    while chunk := await res.content.read(1024):
                        f.write(chunk)

    async def checkFileExist(self):
        for key,val in self.preferDict.items():
            if not path.exists(f"./ota/{val.buildVersion}.zip"):
                await self.download(val.downloadLink, f"./ota/{val.buildVersion}.zip")
