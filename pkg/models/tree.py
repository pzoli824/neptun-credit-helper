
from typing import Generic, TypeVar, Optional, NamedTuple

T = TypeVar("T")

class Connections(NamedTuple):
    parent: 'Optional[Node[T]]'
    children: 'list[Node[T]]'

class Tree(Generic[T]):

    def __init__(self, data: T) -> None:
        self.__node = Node(data, None)

    def insert(self, data: T) -> None:
        self.__node.insert(data)

    @property
    def rootNode(self) -> 'Node[T]':
        self.__node

    def getLeafNodes(self) -> 'list[Node[T]]':
       return self.__findLeafNodes(self.__node.children, list[Node[T]])

    def __findLeafNodes(self, children: 'list[Node[T]]', leafNodes: 'list[Node[T]]') -> 'list[Node[T]]':
        if len(children) < 1:
            return leafNodes
        
        first = children.pop(0)
        children.extend(first.children)

        self.__findLeafNodes(children, leafNodes)


class Node(Generic[T]):

    def __init__(self, data: T, parent: Optional['Node[T]']) -> None:
        self.__data = data
        self.__connections = Connections(parent, list[Node[T]])

    @property
    def data(self) -> T:
        return self.__data
    
    @data.setter 
    def data(self, data: T): 
        self.__data = data

    def insert(self, data: T) -> T:
        self.__connections.children.append(Node(data, self))

    @property
    def parent(self):
        return self.__connections.parent  
    
    @parent.setter 
    def parent(self, parent: 'Node[T]'): 
        self.__connections.parent = parent

    @property
    def children(self) -> 'list[Node[T]]':
        return self.__connections.children       
