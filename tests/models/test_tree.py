import pytest

from pkg.models.tree import Tree

class TestTree:

    def test_new_tree_initilaization_with_string(self):
        initValue = "for testing"
        t = Tree[str](initValue)

        data = t.getFirstNode().getData()
        
        assert initValue == data

    @pytest.mark.skip(reason="need to implement")
    def test_tree_insert_new_element(self):
        pass 

class TestTreeNode:

    @pytest.mark.skip(reason="need to implement")
    def test_new_tree_node_with_parent(self):
        pass

    @pytest.mark.skip(reason="need to implement")
    def test_new_tree_node_without_parent(self):
        pass

    @pytest.mark.skip(reason="need to implement")
    def test_tree_node_insert(self):
        pass