from quart import Quart, send_from_directory
from FileHelper import checkCert, checkdir
from OTAHelper import OTAChecker
from asyncio import create_task


class MyQuart(Quart):
    OTAServer: OTAChecker


app = MyQuart(__name__)
app.OTAServer = OTAChecker()


@app.before_serving
async def startup():
    create_task(app.OTAServer.updateOTAInfo())


@app.get("/ota/<filename>")
async def staticFile(filename: str):
    return await send_from_directory("./ota/", filename)


@app.get("/cert")
async def getCert(filename: str):
    return await send_from_directory("./cert/", "cert.pem")


@app.route("/info")
async def info():
    return app.OTAServer.preferDict


if __name__ == "__main__":
    checkdir()
    checkCert()
    app.run("0.0.0.0", use_reloader=False)
