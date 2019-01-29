from abc import ABC
from enum import Enum

class RelationType(Enum):
    CardinalRelation = "CardinalRelation"
    TopologicalRelation = "TopologicalRelation"
    DistanceRelation = "DistanceRelation"

class CardinalRelationName(Enum):
    North = "North"
    South = "South"
    West = "West"
    East = "East"
    NorthEast = "NorthEast"
    NorthWest = "NorthWest"
    SouthEast = "SouthEast"
    SouthWest = "SouthWest"

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

class NorthEastCardinalRelation(CardinalRelation):
    name = CardinalRelationName.NorthEast

class NorthWestCardinalRelation(CardinalRelation):
    name = CardinalRelationName.NorthWest

class SouthEastCardinalRelation(CardinalRelation):
    name = CardinalRelationName.SouthEast

class SouthWestCardinalRelation(CardinalRelation):
    name = CardinalRelationName.SouthWest

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

