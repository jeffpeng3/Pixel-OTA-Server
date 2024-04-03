# OTA Server For Pixel

`OTA Server For Pixel` is a [Custota](https://github.com/chenxiaolong/Custota)'s OTA Server, used to regularly check and download the latest OTA from Google, use lastest `custota-tool` to generate csig and json, which can be accomplished by simply running this docker image.

## Usage

1. Deploy this image.
2. Fill in `http(s)://your.domain/ota` in `Custota`'s OTA installation source.
3. Download the certificate for verifying csig at `http(s)://your.domain/cert.pem`.
4. Enable [`Custota` debugmode](https://github.com/chenxiaolong/Custota?tab=readme-ov-file#debug-mode)
5. Install the cert.pem you just downloaded as a csig certificate.
6. Congratulations on completing your setup!

## Docker cli

### Deploy command

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

|              Parameter               | Description                                                                          |
| :----------------------------------: | ------------------------------------------------------------------------------------ |
|              `-p 5000`               | HTTP API endpoint.                                                                   |
|      `-v /path/to/ota:/app/ota`      | Mount the OTA update file volume, including the certificate ota.pem for OTA updates. |
|     `-v /path/to/cert:/app/cert`     | Mount a volume for storing certificates needed for verify csig.                      |
|        `-e COUNTRY_NAME="TW"`        | Country code for certificates.                                                       |
|     `-e LOCALITY_NAME="Taipei"`      | City name for certificates.                                                          |
|    `-e DEVICE_CODE_NAME="hysky"`     | Device code that you want to use.                                                    |
|   `-e COMMON_NAME="mydomain.com"`    | Common name for certificates.                                                        |
|  `-e ORGANIZATION_NAME="MyCompany"`  | Organization's name for certificates.                                                |
| `-e STATE_OR_PROVINCE_NAME="Taiwan"` | State or province name for certificates.                                             |
