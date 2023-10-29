
from typing import Generic, TypeVar, Optional

T = TypeVar("T")

class Tree(Generic[T]):

    def __init__(self, data: T) -> None:
        self.__root = TreeNode[T](data, None)
        self.__nodes: list['TreeNode[T]']

    def add(self, data: T) -> None:
        node = TreeNode(data, self.__root)
        self.__nodes.append(node)

    def getFirstNode(self) -> 'TreeNode[T]':
        return self.__root     
        

class TreeNode(Generic[T]):

    def __init__(self, data: T, parent: Optional['TreeNode[T]']) -> None:
        self.__parent = parent
        self.__data = data
        self.__nodes = list[TreeNode[T]]

    def add(self, data: T) -> None:
        node = TreeNode(data, self.__parent)
        self.__nodes.append(node)

    def getData(self) -> T:
        return self.__data   