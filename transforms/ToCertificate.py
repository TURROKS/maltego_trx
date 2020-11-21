from maltego_trx.transform import DiscoverableTransform
import requests
import re
import datetime as dt

__author__ = 'Mario Rojas'
__credits__ = []
__license__ = 'MIT'
__version__ = '1.1.0'
__maintainer__ = 'Mario Rojas'
__email__ = 'mario.rojas-chinchilla@outlook.com'
__status__ = 'Development'


class ToCertificate(DiscoverableTransform):
    """
    Lookup the ssl certificate associated with a domain.
    """

# The Following Function handles the entity creation based on the data received from the request and get_certs
    @classmethod
    def create_entities(cls, request, response):
        domain = request.Value

        try:
            data = cls.get_certs(domain)

            for key in data.json():

                issuer = re.findall(r'CN=(.+)', key['issuer_name'])
                expiration = dt.datetime.strptime(key['not_after'], "%Y-%m-%dT%H:%M:%S")

                ent = response.addEntity('maltego.SSLCertificate', key['id'])
                ent.addProperty(fieldName='cert_subject', displayName='Certificate Subject', value=key['name_value'])
                ent.addProperty(fieldName='cert_issuer', displayName='Certificate Issuer', value=issuer[0])
                ent.addProperty(fieldName='cert_issuer_id', displayName='Certificate Issuer ID', value=key['issuer_ca_id'])
                ent.addProperty(fieldName='cert_expiry', displayName='Certificate Expiry Date', value=expiration)
                ent.setWeight(10)
                if expiration < dt.datetime.now():
                    ent.setBookmark(bookmark=4)
                else:
                    pass

        except ConnectionError:
            response.addUIMessage("Connection Error")

# The get_certs function is the that queries the crt.sh API and gets the required data for the transform
    @staticmethod
    def get_certs(search_domain):

        data = requests.get("https://crt.sh/?CN={}&output=json".format(search_domain))

        if data.status_code == 200:
            return data
        else:
            return ConnectionError

# Following section is required only for testing from terminal, will be ignored otherwise


if __name__ == "__main__":
    print(ToCertificate.get_certs("gearsoftcr.com").json())
