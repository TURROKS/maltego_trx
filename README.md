# maltego_trx

This repository contains 2 Maltego Local Transforms that provide details related to SSL Certificates

1. Domain to SSL Certificate: This transform takes a 'maltego.Domain' entity as input and returns a 'maltego.SSLCertificate' entity with the following details, which we gather from https://crt.sh

* Certificate ID
* Certificate Subject
* Certificate Issuer
* Certificate Issuer ID
* Certificate Expiry Date

2. SSL Certificate to Issuer Name: This transform takes a 'maltego.SSLCertificate' entity as input and returns a 'maltego.Phrase' entity with the following details

* Certificate Issuer Name
