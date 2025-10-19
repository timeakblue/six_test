from dataclasses import dataclass, field
from enum import Enum
import uuid
from typing import Optional



class RocketStatus(str, Enum):
  ON_GROUND = "On ground"
  IN_SPACE = "In space"
  IN_REPAIR = "In repair"
  IN_BUILD = "In build"


class MissionStatus(str, Enum):
  SCHEDULED = "Scheduled"
  PENDING = "Pending"
  IN_PROGRESS = "In progress"
  ENDED = "Ended"


@dataclass
class Rocket:
  name: str
  id: str = field(default_factory=lambda: str(uuid.uuid4()))
  status: RocketStatus = RocketStatus.ON_GROUND
  mission_id: Optional[str] = None


@dataclass
class Mission:
  name: str
  id: str = field(default_factory=lambda: str(uuid.uuid4()))
  status: MissionStatus = MissionStatus.SCHEDULED
  rocket_ids: list[str] = field(default_factory=list)
