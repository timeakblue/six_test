#the main source file

from dataclasses import dataclass, field
from typing import Dict, List, Optional



class RocketStatus(str, Enum):
  
class MissionStatus(str, Enum):
  
class RepoError(Exception):
  
class NotFoundError(RepoError):
  
class ValidationError(RepoError):
  
@dataclass
class Rocket:
  
@dataclass
class Mission:
  
class RocketsRepository:
