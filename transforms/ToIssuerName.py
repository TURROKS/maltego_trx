from maltego_trx.entities import Phrase
from maltego_trx.transform import DiscoverableTransform

__author__ = 'Mario Rojas'
__credits__ = []
__license__ = 'MIT'
__version__ = '1.0.1'
__maintainer__ = 'Mario Rojas'
__email__ = 'mario.rojas-chinchilla@outlook.com'
__status__ = 'Development'


class ToIssuerName(DiscoverableTransform):
    """
    Lookup the Issuer Name associated with a ssl certificate.
    """

# The Following Function handles the entity creation based on the data received from the request
    @classmethod
    def create_entities(cls, request, response):

        try:
            name = request.getProperty(key='cert_issuer')
            response.addEntity(Phrase, name)

        except KeyError:
            response.addUIMessage("Invalid Key")
