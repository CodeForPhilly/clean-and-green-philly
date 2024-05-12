from data_utils import utils


class TestUtils:
    """test methods for utility functions"""

    def test_mask_password(self):
        """test masking password in postgres connect string"""
        url = "postgresql://user:pass@localhost/db"
        masked = utils.mask_password(url)
        assert masked == "postgresql://user:MASKED@localhost/db"
