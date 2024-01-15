
from typing import Generic, TypeVar, Optional, NamedTuple

T = TypeVar("T")

class Connections(NamedTuple):
    parent: Optional['Node[T]']
    children: list['Node[T]']

class Tree(Generic[T]):

    def __init__(self, data: T) -> None:
        self._node = Node[T](data)

    @property
    def root_node(self) -> 'Node[T]':
        return self._node

    def append_child_nodes(self, *nodes: 'Node[T]') -> None:
        self._node.append_child_nodes(*nodes)

    def get_leaf_nodes(self) -> 'list[Node[T]]':
       return self._find_leaf_nodes(self._node.children[:], list[Node[T]]())

    def get_leaf_nodes_data(self) -> list[T]:
        leaf_nodes = self.get_leaf_nodes()
        return [node.data for node in leaf_nodes]

    def _find_leaf_nodes(self, children: 'list[Node[T]]', leaf_nodes: 'list[Node[T]]') -> 'list[Node[T]]':
        if len(children) == 0:
            return leaf_nodes
        
        first_node = children.pop(0)
        children.extend(first_node.children)

        if len(first_node.children) == 0:
            leaf_nodes.append(first_node)

        return self._find_leaf_nodes(children, leaf_nodes)


class Node(Generic[T]):

    def __init__(self, data: T) -> None:
        self._data = data
        self._connections = Connections(None, list[Node[T]]())

    @property
    def data(self) -> T:
        return self._data
    
    @data.setter 
    def data(self, data: T): 
        self._data = data

    def append_child_nodes(self, *nodes: 'Node[T]') -> None:
        for node in nodes:
            node.parent = self
            self._connections.children.append(node)

    @property
    def parent(self):
        return self._connections.parent  
    
    @parent.setter 
    def parent(self, parent: 'Node[T]'): 
        self._connections = Connections(parent, self._connections.children)

    @property
    def children(self) -> list['Node[T]']:
        return self._connections.children       

    def __str__(self):
        has_children = len(self._connections.children) > 0 if "YES" else "NO"
        has_parent = self._connections.parent != None if "YES" else "NO"
        return f"This node has children: {has_children}, and has parent: {has_parent} " + str(self.data)