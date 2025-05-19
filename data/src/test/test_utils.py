import re

from src.data_utils import utils


class TestUtils:
    """test methods for utility functions"""

    def test_mask_password(self):
        """test masking password in postgres connect string"""
        url = "postgresql://user:pass@localhost/db"
        masked = utils.mask_password(url)
        assert masked == "postgresql://user:MASKED@localhost/db"

    def test_clean_diff_output(self):
        output = """582970 rows in table A
582971 rows in table B
1 rows exclusive to table A (not present in B)
2 rows exclusive to table B (not present in A)
1054 rows updated
581915 rows unchanged
0.18% difference score

Extra-Info:
  diff_counts = {'parcel_number_a': 0, 'market_value_a': 6, 'sale_date_a': 2,
'sale_price_a': 18, 'geometry_a': 227}
  exclusive_count = 0
  table1_count = 582970
  table1_sum_market_value = 208050733241.0
  table1_sum_sale_price = 179146818737.0
  table2_count = 582971
  table2_sum_market_value = 208057414341.0
  table2_sum_sale_price = 179117255564.0"""
        cleaned = re.sub(r"\n\nExtra-Info:.*", "", output, flags=re.DOTALL)
        assert (
            cleaned
            == """582970 rows in table A
582971 rows in table B
1 rows exclusive to table A (not present in B)
2 rows exclusive to table B (not present in A)
1054 rows updated
581915 rows unchanged
0.18% difference score"""
        )
