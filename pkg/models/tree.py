
from typing import Generic, TypeVar, Optional, NamedTuple

T = TypeVar("T")

class Connections(NamedTuple):
    parent: Optional['Node[T]']
    children: list['Node[T]']

class Tree(Generic[T]):

    def __init__(self, data: T) -> None:
        self.__node = Node[T](data)

    @property
    def rootNode(self) -> 'Node[T]':
        return self.__node

    def appendChildNodes(self, *nodes: 'Node[T]') -> None:
        self.__node.appendChildNodes(*nodes)

    def getLeafNodes(self) -> 'list[Node[T]]':
       return self.__findLeafNodes(self.__node.children[:], list[Node[T]]())

    def getLeafNodesData(self) -> list[T]:
        leafNodes = self.getLeafNodes()
        return [node.data for node in leafNodes]

    def __findLeafNodes(self, children: 'list[Node[T]]', leafNodes: 'list[Node[T]]') -> 'list[Node[T]]':
        if len(children) == 0:
            return leafNodes
        
        firstNode = children.pop(0)
        children.extend(firstNode.children)

        if len(firstNode.children) == 0:
            leafNodes.append(firstNode)

        return self.__findLeafNodes(children, leafNodes)


class Node(Generic[T]):

    def __init__(self, data: T) -> None:
        self.__data = data
        self.__connections = Connections(None, list[Node[T]]())

    @property
    def data(self) -> T:
        return self.__data
    
    @data.setter 
    def data(self, data: T): 
        self.__data = data

    def appendChildNodes(self, *nodes: 'Node[T]') -> None:
        for node in nodes:
            node.parent = self
            self.__connections.children.append(node)

    @property
    def parent(self):
        return self.__connections.parent  
    
    @parent.setter 
    def parent(self, parent: 'Node[T]'): 
        self.__connections = Connections(parent, self.__connections.children)

    @property
    def children(self) -> list['Node[T]']:
        return self.__connections.children       
