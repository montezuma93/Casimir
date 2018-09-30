from abc import ABC

class Relation(ABC):

    def __init__(self):
        pass

class RelationCategorie(Relation):

    def __init__(self, category_name, amountOfObjects):
        self.category_name = category_name
        self.amountOfObjects = amountOfObjects
        super().__init__()

class CardinalRelation(RelationCategorie):
    def __init__(self):
        super().__init__("CardinalRelation", 2)

class NorthCardinalRelation(CardinalRelation):
    def __init__(self):
        self.name = "North"
        super().__init__()

class SouthCardinalRelation(CardinalRelation):
    def __init__(self):
        self.name = "South"
        super().__init__()

class WestCardinalRelation(CardinalRelation):
    def __init__(self):
        self.name = "West"
        super().__init__()

class EastCardinalRelation(CardinalRelation):
    def __init__(self):
        self.name = "East"
        super().__init__()

class SpatialRelation(RelationCategorie):
    def __init__(self):
        super().__init__("SpatialRelation", 2)

class LeftSpatialRelation(SpatialRelation):
    def __init__(self):
        self.name = "Left"
        super().__init__()    

class RightSpatialRelation(SpatialRelation):
    def __init__(self):
        self.name = "Right"
        super().__init__()

class UpSpatialRelation(SpatialRelation):
    def __init__(self):
        self.name = "Up"
        super().__init__()

class DownSpatialRelation(SpatialRelation):
    def __init__(self):
        self.name = "Down"
        super().__init__()    

class TopologicalRelation(RelationCategorie):
    def __init__(self):
        super().__init__("TopologicalRelation", 2)

class PartOfTopologicalRelation(TopologicalRelation):
    def __init__(self):
        self.name = "PartOf"
        super().__init__()    

class DistanceRelation(RelationCategorie):
    def __init__(self):
        super().__init__("DistanceRelation", 2)

class FarSpatialRelation(DistanceRelation):
    def __init__(self):
        self.name = "Far"
        super().__init__()    

class CloseSpatialRelation(DistanceRelation):
    def __init__(self):
        self.name = "Clase"
        super().__init__()    
