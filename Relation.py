from abc import ABC

class Relation(ABC):
    def __init__(self):
        pass

class RelationCategorie(Relation):
    pass

class CardinalRelation(RelationCategorie):
    category_name = "CardinalRelation"
    amount_of_objects = 2

class NorthCardinalRelation(CardinalRelation):
    name = "North"

class SouthCardinalRelation(CardinalRelation):
    name = "South"

class WestCardinalRelation(CardinalRelation):
    name = "West"

class EastCardinalRelation(CardinalRelation):
    name = "East"

class SpatialRelation(RelationCategorie):
    category_name = "SpatialRelation"
    amount_of_objects = 2

class LeftSpatialRelation(SpatialRelation):
    name = "Left" 

class RightSpatialRelation(SpatialRelation):
    name = "Right" 

class UpSpatialRelation(SpatialRelation):
    name = "Up"

class DownSpatialRelation(SpatialRelation):
    name = "Down"

class TopologicalRelation(RelationCategorie):
    category_name = "TopologicalRelation"
    amount_of_objects = 2

class PartOfTopologicalRelation(TopologicalRelation):
    name = "PartOf"   

class DistanceRelation(RelationCategorie):
    category_name = "DistanceRelation"
    amount_of_objects = 2

class FarSpatialRelation(DistanceRelation):
    name = "Far"

class CloseSpatialRelation(DistanceRelation):
    name = "Close"
