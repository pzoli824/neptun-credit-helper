import pytest

from pkg.models.tree import Tree

class TestTree:

    def test_new_tree_with_string(self):
        initValue = "for testing"
        t = Tree[str](initValue)
        data = t.getFirstNode().getData()
        
        self.assertEqual(initValue, data, "initialization value and after instantiation value is different")

