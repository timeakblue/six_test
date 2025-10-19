# test file
import pytest
from .dragon_repo import SpaceXRepository
from .models import RocketStatus, MissionStatus
#from .exceptions import #(errors) InvalidOperationError, NotFoundError



@pytest.fixture
def repo():
  return SpaceXRepository()


def test_add_and_get_rocket(repo):
  r = repo.add_rocket("Dragon 1")
  assert r.name == "Dragon 1"
  assert r.status == RocketStatus.ON_GROUND
  assert repo.get_rocket(r.id).id == r.id


def test_add_and_get_mission(repo):
  m = repo.add_mission("Mars")
  assert m.name == "Mars"
  assert m.status == MissionStatus.SCHEDULED
  assert repo.get_mission(m.id).id == m.id


def test_assign_rocket_to_mission_and_status_changes(repo):
  r = repo.add_rocket("Red Dragon")
  m = repo.add_mission("Transit")
  repo.assign_rocket_to_mission(r.id, m.id)
  # after assignment, mission should be In progress (rocket still On ground, but assigned and none in repair)
  assert repo.get_mission(m.id).status in (MissionStatus.IN_PROGRESS, MissionStatus.PENDING)
  # change rocket to In repair -> mission becomes Pending
  repo.change_rocket_status(r.id, RocketStatus.IN_REPAIR)
  assert repo.get_mission(m.id).status == MissionStatus.PENDING


def test_cannot_assign_same_rocket_twice(repo):
  r = repo.add_rocket("D")
  m1 = repo.add_mission("A")
  m2 = repo.add_mission("B")
  repo.assign_rocket_to_mission(r.id, m1.id)
  with pytest.raises(InvalidOperationError):
  repo.assign_rocket_to_mission(r.id, m2.id)


def test_cannot_assign_to_ended_mission(repo):
  r = repo.add_rocket("D")
  m = repo.add_mission("A")
  # mission must have zero rockets to be ended
  repo.change_mission_status(m.id, MissionStatus.ENDED)
  with pytest.raises(InvalidOperationError):
  repo.assign_rocket_to_mission(r.id, m.id)


def test_change_mission_to_ended_requires_zero_rockets(repo):
  r = repo.add_rocket("D")
  m = repo.add_mission("A")
  repo.assign_rocket_to_mission(r.id, m.id)
  with pytest.raises(InvalidOperationError):
  repo.change_mission_status(m.id, MissionStatus.ENDED)
  # unassign and then end
  repo.u
