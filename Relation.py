from abc import ABC
from enum import Enum

class RelationType(Enum):
    CardinalRelation = 1
    SpatialRelation = 2
    TopologicalRelation = 3
    DistanceRelation = 4

class CardinalRelationName(Enum):
    North = 1
    South = 2
    West = 3
    East = 4

class SpatialRelationName(Enum):
    Left = 1
    Right = 2
    Up = 3
    Down = 4

class TopologicalRelationName(Enum):
    PartOf = 1

class DistanceRelationName(Enum):
    Far = 1
    Close = 2

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

class FarSpatialRelation(DistanceRelation):
    name = DistanceRelationName.Far

class CloseSpatialRelation(DistanceRelation):
    name = DistanceRelationName.Close

