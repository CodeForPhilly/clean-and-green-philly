from data_utils.park_priority import park_priority
from data_utils.ppr_properties import ppr_properties
from data_utils.vacant_properties import vacant_properties

class TestDataUtils:
    """
    test methods for data utils feature layer classes
    """
    def test_park_priority(self):
        """ test the park priority layer.  Simply construct the class for now to see if it works.
        """        
        park_priority(vacant_properties())

    def test_ppr_properties(self):
        """ test the ppr properties layer.  Simply construct the class for now to see if it works.
        """        
        ppr_properties(vacant_properties())        