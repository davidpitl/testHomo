"""A module to keep track of a ciphertext."""

from util.public_key import PublicKey
from util.polynomial import Polynomial

class Ciphertext:

    """An instance of a ciphertext.

    This is a wrapper class for a ciphertext, which consists
    of two polynomial.

    Attributes:
        c0 (Polynomial): First element of ciphertext.
        c1 (Polynomial): Second element of ciphertext.
        scaling_factor (float): Scaling factor.
        modulus (int): Ciphertext modulus.
    """

    def __init__(self, c0=None, c1=None, scaling_factor=None, modulus=None,s=None):
        """Sets ciphertext to given polynomials.

        Args:
            c0 (Polynomial): First element of ciphertext.
            c1 (Polynomial): Second element of ciphertext.
            scaling_factor (float): Scaling factor. Can be None for BFV.
            modulus (int): Ciphertext modulus. Can be None for BFV.
        """
        
        if s!=None:
            k=PublicKey()
            (a,b)=s.split("+")
            c0=Polynomial(s=a.split("=")[1])
            c1=Polynomial(s=b.split("=")[1]) 
            scaling_factor=None
            modulus=None
        
        
        self.c0 = c0
        self.c1 = c1
        self.scaling_factor = scaling_factor
        self.modulus = modulus

    def __str__(self):
        """Represents Ciphertext as a string.

        Returns:
            A string which represents the Ciphertext.
        """
        return 'c0=' + str(self.c0) + '+c1=' + str(self.c1)
    
    
    # def getPartial(self,ini):
    #     return Ciphertext(self.c0.getPartial(ini),self.c1.getPartial(ini),self.scaling_factor,self.modulus)
        
