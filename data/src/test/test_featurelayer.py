from classes.featurelayer import FeatureLayer
from config.config import tiles_file_id_prefix

class TestFeaturelayer:
    """ Tests for the feature layer class
    """    
    def test_tiles_file_size_ok(self):
        """ test that the size of the tiles file exceeds a minimum.  
        Assumes a temp file is there from a previous run.
        """
        test_fl = FeatureLayer("test")
        # it should be smaller than 10 MB
        assert not test_fl.tiles_file_size_ok(f"tmp/temp_{tiles_file_id_prefix}_merged.pmtiles", 10 * 1024 * 1024) 
        # but bigger than 1 KB
        assert test_fl.tiles_file_size_ok(f"tmp/temp_{tiles_file_id_prefix}_merged.pmtiles", 1024 ) 