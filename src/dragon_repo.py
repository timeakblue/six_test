from typing import Dict, List
from .models import Rocket, Mission, RocketStatus, MissionStatus
from .exceptions import NotFoundError, InvalidOperationError


class SpaceXRepository:
  def __init__(self) -> None:
    self._rockets: Dict[str, Rocket] = {}
    self._missions: Dict[str, Mission] = {}

  # Rockets
  def add_rocket(self, name: str) -> Rocket:
    rocket = Rocket(name=name)
    self._rockets[rocket.id] = rocket
    return rocket

  def get_rocket(self, rocket_id: str) -> Rocket:
    try:
      return self._rockets[rocket_id]
    except KeyError:
      raise NotFoundError(f"Rocket {rocket_id} not found")

  def change_rocket_status(self, rocket_id: str, new_status: RocketStatus) -> Rocket:
    rocket = self.get_rocket(rocket_id)
    rocket.status = new_status
    if rocket.mission_id:
      self._recompute_mission_status(rocket.mission_id)
    return rocket

  # Missions
  def add_mission(self, name: str) -> Mission:
    mission = Mission(name=name)
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
  rocket.mission_id = mission.id
  mission.rocket_ids.append(rocket.id)
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
  self._recompute_mission_status(mission.id)
  rocket.mission_id = None

def change_mission_status(self, mission_id: str, new_status: MissionStatus) -> Mission:
  mission = self.get_mission(mission_id)
  if new_status == MissionStatus.ENDED and mission.rocket_ids:
  raise InvalidOperationError("Cannot mark mission as Ended while rockets are assigned")
  mission.status = new_status
  return mission

  # Queries
def get_missions_summary(self) -> List[Mission]:
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
  return
  if not mission.rocket_ids:
  mission.status = MissionStatus.SCHEDULED
  return
  rockets = [self._rockets[rid] for rid in mission.rocket_ids if rid in self._rockets]
  if any(r.status == RocketStatus.IN_REPAIR for r in rockets):
  mission.status = MissionStatus.PENDING
  else:
  mission.status = MissionStatus.IN_PROGRESS
