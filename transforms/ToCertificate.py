from maltego_trx.transform import DiscoverableTransform
import requests
import re

__author__ = 'Mario Rojas'
__credits__ = []
__license__ = 'MIT'
__version__ = '1.0'
__maintainer__ = 'Mario Rojas'
__email__ = 'mario.rojas-chinchilla@outlook.com'
__status__ = 'Development'


class ToCertificate(DiscoverableTransform):
    """
    Lookup the ssl certificate associated with a domain.
    """

    @classmethod
    def create_entities(cls, request, response):
        domain = request.Value

        try:
            data = cls.get_certs(domain)

            for key in data.json():

                ent = response.addEntity('maltego.SSLCertificate', key['id'])
                ent.setWeight(10)
                issuer = re.findall(r'CN=(.+)', key['issuer_name'])
                ent.addProperty(fieldName='cert_subject', displayName='Certificate Subject', value=key['name_value'])
                ent.addProperty(fieldName='cert_issuer', displayName='Certificate Issuer', value=issuer[0])
                ent.addProperty(fieldName='cert_issuer_id', displayName='Certificate Issuer ID', value=key['issuer_ca_id'])
                ent.addProperty(fieldName='cert_expiry', displayName='Certificate Expiry Date', value=key['not_after'])

        except ConnectionError:
            response.addUIMessage("Connection Error")

    @staticmethod
    def get_certs(search_domain):

        data = requests.get("https://crt.sh/?CN={}&output=json".format(search_domain))

        if data.status_code == 200:
            return data
        else:
            return ConnectionError


if __name__ == "__main__":
    print(ToCertificate.get_certs("gearsoftcr.com").json())
