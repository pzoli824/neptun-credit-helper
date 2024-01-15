import pytest
import os

from pkg.localization.localization import Language, Localization

class TestLocalization:

    def test_localization_initialization(self):
        path = os.path.dirname(os.path.abspath(__file__))
        
        loc = Localization(f"{path}/localization.yaml", Language.HUNGARY)

        assert loc['group']['group_text'] == "group text"

    def test_localization_wrong_language(self):
        path = os.path.dirname(os.path.abspath(__file__))
        loc = Localization(f"{path}/localization.yaml", "dummy")
        
        with pytest.raises(KeyError) as _:
            loc["dummy"]