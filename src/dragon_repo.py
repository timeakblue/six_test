
from dataclasses import dataclass, field
from typing import Dict, List, Optional

class MissionStatus(str, Enum):
  SCHEDULED = "Scheduled"
  PENDING = "Pending"
  IN_PROGRESS = "In progress"
  ENDED = "Ended"

from .models import Rocket, Mission, RocketStatus, MissionStatus
  self._missions[mission.id] = mission
  return mission


def get_mission(self, mission_id: str) -> Mission:
  try:
  return self._missions[mission_id]
  except KeyError:
  raise NotFoundError(f"Mission {mission_id} not found")


def assign_rocket_to_mission(self, rocket_id: str, mission_id: str) -> None:
  rocket = self.get_rocket(rocket_id)
  mission = self.get_mission(mission_id)
  if mission.status == MissionStatus.ENDED:
  raise InvalidOperationError("Cannot assign rockets to an Ended mission")
  if rocket.mission_id is not None:
  raise InvalidOperationError("Rocket already assigned to a mission")
  # assign
  rocket.mission_id = mission.id
  mission.rocket_ids.append(rocket.id)
  # recompute mission status
  self._recompute_mission_status(mission.id)


def unassign_rocket_from_mission(self, rocket_id: str) -> None:
  rocket = self.get_rocket(rocket_id)
  if not rocket.mission_id:
  return
  mission = self._missions.get(rocket.mission_id)
  if mission:
  try:
  mission.rocket_ids.remove(rocket.id)
  except ValueError:
  pass
  # recompute mission status after removal
  self._recompute_mission_status(mission.id)
  rocket.mission_id = None


def change_mission_status(self, mission_id: str, new_status: MissionStatus) -> Mission:
  mission = self.get_mission(mission_id)
  # Ended constraints
  if new_status == MissionStatus.ENDED and mission.rocket_ids:
  raise InvalidOperationError("Cannot mark mission as Ended while rockets are assigned")
  mission.status = new_status
  return mission


#  Queries 
def get_missions_summary(self) -> List[Mission]:
  """Return missions ordered by number of rockets assigned (desc), ties by name desc alphabetical.
  Missions returned as copies to avoid accidental external mutation.
  """
  missions = list(self._missions.values())
  missions.sort(key=lambda m: (len(m.rocket_ids), m.name), reverse=True)
  return missions


def get_mission_detail(self, mission_id: str) -> Mission:
  return self.get_mission(mission_id)


# Internal helpers 
def _recompute_mission_status(self, mission_id: str) -> None:
  mission = self._missions.get(mission_id)
  if not mission:
  return
  if mission.status == MissionStatus.ENDED:
  # once ended, status remains ended until explicitly changed (but assignments prevented earlier)
  return
  if not mission.rocket_ids:
  mission.status = MissionStatus.SCHEDULED
  return
  # at least one assigned rocket
  rockets = [self._rockets[rid] for rid in mission.rocket_ids if rid in self._rockets]
  if any(r.status == RocketStatus.IN_REPAIR for r in rockets):
  mission.status = MissionStatus.PENDING
  else:
  mission.status = MissionStatus.IN_PROGRESS
