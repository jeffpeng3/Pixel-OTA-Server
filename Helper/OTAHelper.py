from selectolax.lexbor import LexborHTMLParser
from http.cookies import BaseCookie
from asyncio import sleep, create_task, create_subprocess_exec
from asyncio.subprocess import PIPE
from dataclasses import dataclass,field
from aiohttp import ClientSession
from typing import Optional
from re import compile
from os import path, getenv, remove, listdir

deviceCodeName = getenv("DEVICE_CODE_NAME", "husky")

regexPattern = compile(
    r"(\d+\.\d+\.\d+)\s\((\w+\.\w+\.\w+)(\.[^,]+)?,\s(\w+\s\w+)(,\s.+)?\)"
)


@dataclass
class OTAInfo:
    androidVer: str
    buildVer: str
    subVer: Optional[str]
    date: str
    user: Optional[str]
    DLLink: str
    fName: str = field(init=False)

    def __post_init__(self):
        self.fName = self.DLLink.split("/")[-1]


class OTAChecker:
    def __init__(self) -> None:
        self.lastest: Optional[OTAInfo] = None

    async def fetchLastestOTA(self):
        async with ClientSession() as s:
            cookie = BaseCookie({"devsite_wall_acks": "nexus-ota-tos"})
            s.cookie_jar.update_cookies(cookie)
            async with s.get("https://developers.google.com/android/ota") as res:
                soup = LexborHTMLParser(await res.text())
        targets = soup.css(f'tr[id^="{deviceCodeName}"]')
        if len(targets) == 0:
            print("error")
        for target in targets[::-1]:
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
            if info.user is None or "TW" in info.user:
                self.lastest = info
                break
        self.cleanup()
        create_task(self.updateOTAFile())
        await sleep(86400)
        create_task(self.fetchLastestOTA())

    def cleanup(self):
        if self.lastest is None:
            return
        for file in listdir("./ota"):
            if file.startswith(self.lastest.fName):
                continue
            if file.endswith(".json"):
                continue
            if file.endswith(".pem"):
                continue
            remove(f"./ota/{file}")

    async def updateOTAFile(self):
        if self.lastest is None:
            return
        filename = self.lastest.fName
        if not path.exists(f"./ota/{filename}"):
            await self.download()
        if not path.exists(f"./ota/{filename}.csig"):
            await self.genCsig()
        await self.updateOTAInfo()

    async def download(self):
        if self.lastest is None:
            return
        async with ClientSession() as s:
            async with s.get(self.lastest.DLLink) as res:
                with open(f"./ota/{self.lastest.fName}", "wb") as f:
                    while chunk := await res.content.read(1024):
                        f.write(chunk)

    async def genCsig(self):
        if self.lastest is None:
            return
        filename = self.lastest.fName
        proc = await create_subprocess_exec(
            "./custota-tool",
            "gen-csig",
            "--input",
            f"ota/{filename}",
            "-C",
            "ota/ota.pem",
            "-c",
            "cert/cert.pem",
            "-k",
            "cert/privatekey.pem",
            "-o",
            f"ota/{filename}.csig",
            stdout=PIPE,
            stderr=PIPE,
        )
        stdout, stderr = await proc.communicate()
        print(f"=============================[gen-csig exited with {proc.returncode}]=============================")
        if stdout:
            print(f"[stdout]\n{stdout.decode()}",end="")
        if stderr:
            print(f"[stderr]\n{stderr.decode()}",end="")
        print("==================================================================================")

    async def updateOTAInfo(self):
        if self.lastest is None:
            return
        filename = self.lastest.fName
        proc = await create_subprocess_exec(
            "./custota-tool",
            "gen-update-info",
            "-f",
            "ota/husky.json",
            "-l",
            f"{filename}",
            stdout=PIPE,
            stderr=PIPE,
        )
        stdout, stderr = await proc.communicate()
        print(f"========[gen-update-info exited with {proc.returncode}]========")
        if stdout:
            print(f"[stdout]\n{stdout.decode()}",end="")
        if stderr:
            print(f"[stderr]\n{stderr.decode()}",end="")
        print("===============================================")

