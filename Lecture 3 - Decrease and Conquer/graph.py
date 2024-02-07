import ctypes
class Array:
    def __init__(self, size):
        assert size > 0, "Array size must be > 0"
        self._size = size
        PyArrayType = ctypes.py_object*size
        self._elements=PyArrayType()
        self.clear(None)
        self.index = 0
        
    def __len__(self):
        return self._size
        
    def __getitem__(self, index):
        assert index >= 0 and index < len(self), "Array subcript out of range"
        return self._elements[index]
        
    def __setitem__(self, index, value):
        assert index >= 0 and index < len(self), "Array subcript out of range"
        self._elements[index] = value
        
    def clear(self, value):
        for i in range(len(self)):
            self._elements[i] = value
            
    def __repr__(self):
        s = "[ "
        for x in self._elements:
            s = s + str(x) + ', '
        s = s[:-2] + " ]"
        return s
        
    def __iter__(self):
        self._curIndex = 0
        return self
        
    def __next__(self):
        if self._curIndex < len(self._elements):
            entry = self._elements[self._curIndex]
            self._curIndex += 1
            return entry
        else:
            raise StopIteration

class Array2D:
    def __init__(self, numRows, numCols):
        self._theRows = Array(numRows)
        for i in range(numRows):
            self._theRows[i] = Array(numCols)
            
    def __getitem__(self, indexTuple):
        assert len(indexTuple) == 2, "Invalid number of array subscripts."
        row = indexTuple[0]
        col = indexTuple[1]
        assert row >= 0 and row < self.numRows() and col >= 0 and col < self.numCols(), "Array subscript out of range."
        return self._theRows[row][col]
    
    def __setitem__(self, indexTuple, value):
        assert len(indexTuple) == 2, "Invalid number of array subscripts."
        row = indexTuple[0]
        col = indexTuple[1]
        assert row >= 0 and row < self.numRows() and col >= 0 and col < self.numCols(), "Array subscript out of range."
        self._theRows[row][col] = value
    
    def numRows(self):
        return len(self._theRows)
    
    def numCols(self):
        return len(self._theRows[0])
    
    def clear(self, value):
        for row in self._theRows:
            row.clear(value)
    
    def __repr__(self):
        s = ""
        for r in range(self.numRows()):
            for c in range(self.numCols()):
                b = str(self._theRows[r][c])
                s += b+" "
            s += "\n"
        return s

class Matrix(Array2D):
    def scaleBy(self, Scalar):
        for r in range(self.numRows()):
            for c in range(self.numCols()):
                self[r,c] *= Scalar
    def __add__(self, rhsMatrix):
        assert rhsMatrix.numRows() == self.numRows() and rhsMatrix.numCols() == self.numCols(), "Matrix sizes not compatible for the add operation"
        newMatrix = Matrix(self.numRows(),self.numCols())
        for r in range(self.numRows()):
            for c in range(self.numCols()):
                newMatrix[r,c] = self[r,c] + rhsMatrix[r,c]
        return newMatrix
    def __sub__(self, rhsMatrix):
        assert rhsMatrix.numRows() == self.numRows() and rhsMatrix.numCols() == self.numCols(), "Matrix sizes not compatible for the add operation"
        newMatrix = Matrix(self.numRows(),self.numCols())
        for r in range(self.numRows()):
            for c in range(self.numCols()):
                newMatrix[r,c] = self[r,c] - rhsMatrix[r,c]
        return newMatrix
    def transposition(self):
        newMatrix = Matrix(self.numRows(),self.numCols())
        for r in range(self.numRows()):
            for c in range(self.numCols()):
                newMatrix[r,c] = self[c,r]
        return newMatrix
    def __mul__(self, rhsMatrix):
        assert rhsMatrix.numRows() == self.numCols(), "Matrix sizes not compatible for the multiply operation"
        result = Matrix(self.numRows(), rhsMatrix.numCols())
        for r in range(self.numRows()):
            for c in range(rhsMatrix.numCols()):
                dot_product = sum(self[r, k] * rhsMatrix[k, c] for k in range(self.numCols()))
                result[r, c] = dot_product
        return result
    

class Graph:
    def __init__(self,maxVertices,directed=False):
        self._Vertices = list()
        self._MATRIX = Matrix(maxVertices,maxVertices)
        self._MATRIX.clear(None)
        self._directed = directed
#------------------------- Vertex class -----------------------
    class Vertex:
        __slots__ = '_element'

        def __init__(self, x):
            self._element = x

        def element(self):
            return self._element
        
        def __repr__(self):
            return str(self._element)
#------------------------- Edge class -------------------------
    class Edge:
        __slots__ = '_origin' , '_destination', '_element'

        def __init__(self, u, v, w):
            self._origin = u
            self._destination = v #ปลายทาง
            self._element = w

        def endpoints(self):
            return (self._origin, self._destination)

        def opposite(self, v):
            return self._destination if v is self._origin else self._origin

        def element(self):
            return self._element
        
        def __repr__(self):
            return str(self._element)
#-----------------------------------------------------------
    def is_directed(self): #True / False
        return self._directed

    def findindex(self,v):
        if v in self._Vertices:
            return self._Vertices.index(v)
#-------------------------------------------------------------------------        
    def vertex_count(self): #element in listr
        return len(self._Vertices)
    
    def vertices(self): # list
        return self._Vertices
    
    def edge_count(self):
        total = 0
        for row in range(self.vertex_count()):
            for col in range(self.vertex_count()):
                if self._MATRIX[row,col] != None:
                    total += 1
        return total if self.is_directed() else total // 2 #มีทิศหารออก

    def edges(self):
        edges_list = list()
        for row in range(self.vertex_count()):
            for col in range(self.vertex_count()):
                if (self._MATRIX[row,col] not in edges_list) and (self._MATRIX[row,col] is not None):
                    edges_list.append(self._MATRIX[row,col])
        return edges_list
    
    def get_edge(self, u, v):
        return self._MATRIX[self.findindex(u),self.findindex(v)]
    
    def degree(self, v, outgoing=True):
        total = 0
        if outgoing:
            for col in range(self.vertex_count()):
                if self._MATRIX[self.findindex(v),col] != None:
                    total += 1
        #incoming
        else:
            for row in range(self.vertex_count()):
                if self._MATRIX[row,self.findindex(v)] != None:
                    total += 1
                    
        return total

    def incident_edges(self, v, outgoing=True):
        adj = list()
        if outgoing:
            for col in range(self.vertex_count()):
                if self._MATRIX[self.findindex(v),col] != None:
                    adj.append(self._MATRIX[self.findindex(v),col])
        #incoming
        else:
            for row in range(self.vertex_count()):
                if self._MATRIX[row,self.findindex(v)] != None:
                    adj.append(self._MATRIX[row,self.findindex(v)])
        return adj
    def insert_vertex(self, x):
        v = self.Vertex(x)
        self._Vertices.append(v)
        return v

    def insert_edge(self, u, v, x):
        # u is origin
        # v is destination
        e = self.Edge(u, v, x)
        if self.is_directed():
            self._MATRIX[self.findindex(u),self.findindex(v)] = e
        else:
            self._MATRIX[self.findindex(u),self.findindex(v)] = e
            self._MATRIX[self.findindex(v),self.findindex(u)] = e
        return e

    def remove_vertex(self, v):
        element = self.incident_edges(v) 
        k = self.findindex(v) 
        for i in element:
            self.remove_edge(i)
        
        for i in range(self.vertex_count()): ##ขยับซ้าย
            for j in range(k,self.vertex_count()-1):
                self._MATRIX[i,j],self._MATRIX[i,j+1] = self._MATRIX[i,j+1],self._MATRIX[i,j]
                
        for i in range(k,self.vertex_count()-1): ##ขยับบน
            for j in range(self.vertex_count()):
                self._MATRIX[i,j],self._MATRIX[i+1,j] = self._MATRIX[i+1,j],self._MATRIX[i,j]    
        
        self._Vertices.pop(k)
        
        
        
    def remove_edge(self,e):
        u, v = e.endpoints() ##หา index ตัวที่ลบ
        self._MATRIX[self.findindex(u), self.findindex(v)] = None
        if not self.is_directed():
            self._MATRIX[self.findindex(v), self.findindex(u)] = None

            
    def __repr__(self):
        s = '['
        for r in range(self._MATRIX.numRows()):
            for c in self._MATRIX._theRows[r]:
                if c is None:
                    c = 0
                s = s + str(c) + ',\t '
            s = s[:-2] + ' \n '
        s = s[:-3] + ' ]'
        return s
    
class Graph_Traversal(Graph):
    #def __init__(self,m)
    def DFS(g,u,discovered):
        print(u)
        for e in g.incident_edges(u):
            v = e.opposite(u)
            if v not in discovered:
                discovered[v] = e
                DFS(g,v,discovered)
    def BFS(g, s, discovered):
        level = [s]
        while len(level) > 0:
            next_level= []
            for u in level:
                print(u)
                for e in g.incident_edges(u):
                    v = e.opposite(u)
                    if v not in discovered:
                        discovered[v] = e
                        next_level.append(v)
                level = next_level
    