
import json

from orb.api.error_codes import *
from tastypie.exceptions import BadRequest

class ORBAPIBadRequest(BadRequest):
    
    def __init__(self, error_code):
        
        # Call the base class constructor with the parameters it needs
        error = {"code": error_code, "message": ERROR_CODES[error_code]}
        
        super(ORBAPIBadRequest, self).__init__(json.dumps(error))