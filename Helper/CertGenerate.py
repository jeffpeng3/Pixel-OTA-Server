from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from os import getenv, listdir, remove, path
from cryptography.x509.oid import NameOID
from datetime import datetime, timedelta
from cryptography import x509
from datetime import timezone

UTC = timezone.utc


def generateCert():
    # Key generation
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    # Various details about the certificate
    subject = issuer = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, getenv("COUNTRY_NAME", "TW")),
            x509.NameAttribute(
                NameOID.STATE_OR_PROVINCE_NAME,
                getenv("STATE_OR_PROVINCE_NAME", "Taiwan"),
            ),
            x509.NameAttribute(
                NameOID.LOCALITY_NAME, getenv("LOCALITY_NAME", "Taipei")
            ),
            x509.NameAttribute(
                NameOID.ORGANIZATION_NAME, getenv("ORGANIZATION_NAME", "MyCompany")
            ),
            x509.NameAttribute(
                NameOID.COMMON_NAME, getenv("COMMON_NAME", "mydomain.com")
            ),
        ]
    )

    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.now(UTC))
        .not_valid_after(datetime.now(UTC) + timedelta(days=3650))
        .sign(key, hashes.SHA256())
    )

    # Write the certificate and key to files
    with open("cert/cert.pem", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

    with open("cert/privatekey.pem", "wb") as f:
        f.write(
            key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )
    if path.exists("ota"):
        for i in listdir("ota"):
            if i.endswith(".csig"):
                remove(f"ota/{i}")


if __name__ == "__main__":
    generateCert()
    print("Certificate generated successfully.")
