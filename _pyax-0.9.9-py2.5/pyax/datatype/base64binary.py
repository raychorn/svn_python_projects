"""A simple holder object for binary objects that are to be base64 encoded.
"""
import base64

class ApexBase64Binary:
    """ Holds a binary object that is converted to base64 encoded string 
    on demand
    
    Object will be held in its binary form until the holder is coerced 
    implicitly or explicitly as a string.
    
    Access to the original object is through the instance member binaryObject
    """
    
    def __init__(self, binary_object):
        """
        @param binary_object: binary object to hold
        """
        self.binary_object = binary_object
        return
    
    @classmethod
    def from_encoded_string(cls, encoded_str):
        """ Create an ApexBase64Binary instance from a base64 encoded string
        
        @param encoded_str: base64 encoded binary object
        
        @return: ApexBase64Binary instance
        @rtype: ApexBase64Binary
        """
        binary_object = base64.b64decode(encoded_str)
        return cls(binary_object)
    
    def __str__(self):
        """ Convert the binary object to a base64 encoded string
        
        @return: base65 enocded object
        @rtype: String
        """
        return base64.b64encode(self.binary_object)
    
    pass
        