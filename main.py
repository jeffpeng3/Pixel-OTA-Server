from quart import Quart, send_from_directory, redirect, request
from Helper.FileHelper import checkCert, checkdir
from Helper.OTAHelper import OTAChecker
from asyncio import create_task
from re import compile



class MyQuart(Quart):
    OTAServer: OTAChecker


app = MyQuart(__name__)
app.OTAServer = OTAChecker()


@app.before_serving
async def startup():
    create_task(app.OTAServer.fetchLastestOTA())


@app.get("/ota/<filename>")
async def staticFile(filename: str):
    return await send_from_directory("./ota/", filename)


@app.get("/cert")
async def redirectCert():
    return redirect("/cert.pem")


@app.get("/cert.pem")
async def getCert():
    return await send_from_directory(
        "./cert/", "cert.pem", attachment_filename="cert.pem"
    )


@app.route("/info")
async def info():
    return str(app.OTAServer.lastest)

checkdir()
checkCert()
app.run("0.0.0.0", use_reloader=False)
