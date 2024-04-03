# Pixel OTA Server

`Pixel OTA Server` is a [Custota](https://github.com/chenxiaolong/Custota)'s OTA Server

## Features

- Automatically generate certificates if they do not exist
- Automatically download the latest OTA image
- Automatically extract OTA certificates
- Sign csig and generate json on download
- All of the above features are available out of the box with [a simple command](https://github.com/jeffpeng3/Pixel-OTA-Server?tab=readme-ov-file#Simplest-deploy-command).

## Usage

1. Deploy this image.
2. Fill in `http(s)://your.domain/ota` in `Custota`'s OTA installation source.
3. Download the certificate for verifying csig at `http(s)://your.domain/cert.pem`.
4. Enable [`Custota` debugmode](https://github.com/chenxiaolong/Custota?tab=readme-ov-file#debug-mode)
5. Install the cert.pem you just downloaded as a csig certificate.
6. Congratulations on completing your setup!

## Docker cli

### Simplest deploy command

```bash
docker run -d -p 5000 ghcr.io/jeffpeng3/pixel-custota-ota-server:latest
```

### Full deploy command

```bash
docker run -d \
 --name=OTA-Server \
 -p 5000:5000 \
 -v /path/to/ota:/app/ota \
 -v /path/to/cert:/app/cert \
 -e COUNTRY_NAME="TW" \
 -e LOCALITY_NAME="Taipei" \
 -e DEVICE_CODE_NAME="hysky" \
 -e COMMON_NAME="mydomain.com" \
 -e ORGANIZATION_NAME="MyCompany" \
 -e STATE_OR_PROVINCE_NAME="Taiwan" \
 --restart unless-stopped \
 ghcr.io/jeffpeng3/pixel-custota-ota-server:latest
```

### Parameters

Containers are configured using parameters passed at runtime (such as those above). These parameters are separated by a colon and indicate `<external>:<internal>` respectively. For example, `-p 8080:80` would expose port `80` from inside the container to be accessible from the host's IP on port `8080` outside the container.

|              Parameter               |    Required     | Description                                                                          |
| :----------------------------------: | :-------------: | ------------------------------------------------------------------------------------ |
|              `-p 5000`               | Almost Required | HTTP API endpoint.                                                                   |
|      `-v /path/to/ota:/app/ota`      |    Optional     | Mount the OTA update file volume, including the certificate ota.pem for OTA updates. |
|     `-v /path/to/cert:/app/cert`     |    Optional     | Mount a volume for storing certificates needed for verify csig.                      |
|        `-e COUNTRY_NAME="TW"`        |    Optional     | Country code for certificates.                                                       |
|     `-e LOCALITY_NAME="Taipei"`      |    Optional     | City name for certificates.                                                          |
|    `-e DEVICE_CODE_NAME="hysky"`     |    Optional     | Device code that you want to use.                                                    |
|   `-e COMMON_NAME="mydomain.com"`    |    Optional     | Common name for certificates.                                                        |
|  `-e ORGANIZATION_NAME="MyCompany"`  |    Optional     | Organization's name for certificates.                                                |
| `-e STATE_OR_PROVINCE_NAME="Taiwan"` |    Optional     | State or province name for certificates.                                             |
