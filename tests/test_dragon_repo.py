# test file
import pytest
from .dragon_repo import SpaceXRepository
from .models import RocketStatus, MissionStatus
#from .exceptions import #(errors) InvalidOperationError, NotFoundError



@pytest.fixture
def repo():
  return SpaceXRepository()


def test_add_and_get_rocket(repo):



def test_add_and_get_mission(repo):



def test_assign_rocket_to_mission_and_status_changes(repo):



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
