from util.polynomial import Polynomial 


"""A module to keep track of a public key."""

class PublicKey:

    """An instance of a public key.

    The public key consists of a pair of polynomials generated
    from key_generator.py.

    Attributes:
        p0 (Polynomial): First element of public key.
        p1 (Polynomial): Second element of public key.
    """

    def __init__(self, p0=None, p1=None):
        """Sets public key to given inputs.

        Args:
            p0 (Polynomial): First element of public key.
            p1 (Polynomial): Second element of public key.
        """
        self.p0 = p0
        self.p1 = p1

    def __str__(self):
        """Represents PublicKey as a string.

        Returns:
            A string which represents the PublicKey.
        """
        return 'p0=' + str(self.p0) + '+p1=' + str(self.p1)
    
    def deserializa(s_key):
        k=PublicKey()
        (a,b)=s_key.split("+")
        k.p0=Polynomial(s=a.split("=")[1])
        k.p1=Polynomial(s=b.split("=")[1])
        return k
    
# =============================================================================
#     def from_dict(d):       
#         poly_degree    = d['poly_degree']
#         plain_modulus  = d['plain_modulus']
#         ciph_modulus   = d['ciph_modulus']
#         return BFVParameters(poly_degree, plain_modulus, ciph_modulus)
# =============================================================================
      