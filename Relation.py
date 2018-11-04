from abc import ABC
from enum import Enum

class RelationType(Enum):
    CardinalRelation = "CardinalRelation"
    SpatialRelation = "SpatialRelation"
    TopologicalRelation = "TopologicalRelation"
    DistanceRelation = "DistanceRelation"

class CardinalRelationName(Enum):
    North = "North"
    South = "South"
    West = "West"
    East = "East"

class SpatialRelationName(Enum):
    Left = "Left"
    Right = "Right"
    Up = "Up"
    Down = "Down"

class TopologicalRelationName(Enum):
    PartOf = "PartOf"

class DistanceRelationName(Enum):
    Far = "Far"
    Close = "Close"

class Relation(ABC):
    pass

class RelationCategory(Relation):
    pass

class CardinalRelation(RelationCategory):
    relation_type = RelationType.CardinalRelation
    amount_of_objects = 2

class NorthCardinalRelation(CardinalRelation):
    name = CardinalRelationName.North

class SouthCardinalRelation(CardinalRelation):
    name = CardinalRelationName.South

class WestCardinalRelation(CardinalRelation):
    name = CardinalRelationName.West

class EastCardinalRelation(CardinalRelation):
    name = CardinalRelationName.East

class SpatialRelation(RelationCategory):
    relation_type = RelationType.SpatialRelation
    amount_of_objects = 2

class LeftSpatialRelation(SpatialRelation):
    name = SpatialRelationName.Left

class RightSpatialRelation(SpatialRelation):
    name = SpatialRelationName.Right

class UpSpatialRelation(SpatialRelation):
    name = SpatialRelationName.Up

class DownSpatialRelation(SpatialRelation):
    name = SpatialRelationName.Down

class TopologicalRelation(RelationCategory):
    relation_type = RelationType.TopologicalRelation
    amount_of_objects = 2

class PartOfTopologicalRelation(TopologicalRelation):
    name = TopologicalRelationName.PartOf  

class DistanceRelation(RelationCategory):
    relation_type = RelationType.DistanceRelation
    amount_of_objects = 2

class FarDistanceRelation(DistanceRelation):
    name = DistanceRelationName.Far

class CloseDistanceRelation(DistanceRelation):
    name = DistanceRelationName.Close

