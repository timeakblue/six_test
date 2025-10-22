# test file
import pytest
from typing import List, Dict, Optional, Tuple, Set, Any
from ..src.dragon_repo import SpaceXRepository
from ..src.models import RocketStatus, MissionStatus
from ..src.exceptions import InvalidOperationError, NotFoundError



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
    # change rocket to In repair, then Pending
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
    # mission have zero rockets , ended
    repo.change_mission_status(m.id, MissionStatus.ENDED)
    with pytest.raises(InvalidOperationError):
        repo.assign_rocket_to_mission(r.id, m.id)


def test_change_mission_to_ended_requires_zero_rockets(repo):
    r = repo.add_rocket("D")
    m = repo.add_mission("A")
    repo.assign_rocket_to_mission(r.id, m.id)
    with pytest.raises(InvalidOperationError):
        repo.change_mission_status(m.id, MissionStatus.ENDED)
    # unassign, then end
    repo.unassign_rocket_from_mission(r.id)
    result = repo.change_mission_status(m.id, MissionStatus.ENDED)
    assert result.status == MissionStatus.ENDED


def test_rocket_auto_status_change_on_assignment(repo):
    """test that rocket status automatically changes to IN_SPACE when assigned to mission"""
    r = repo.add_rocket("Dragon 1")
    m = repo.add_mission("Mars Mission")
    
    # initially on ground
    assert r.status == RocketStatus.ON_GROUND
    
    # after assignment, should be in space
    repo.assign_rocket_to_mission(r.id, m.id)
    updated_rocket = repo.get_rocket(r.id)
    assert updated_rocket.status == RocketStatus.IN_SPACE


def test_rocket_auto_status_change_on_unassignment(repo):
    """tTest that rocket status returns to ON_GROUND when unassigned from mission"""
    r = repo.add_rocket("Dragon 1")
    m = repo.add_mission("Mars Mission")
    
    # assign and verify in space
    repo.assign_rocket_to_mission(r.id, m.id)
    assert repo.get_rocket(r.id).status == RocketStatus.IN_SPACE
    #unassign and verify 
    repo.unassign_rocket_from_mission(r.id)
    assert repo.get_rocket(r.id).status == RocketStatus.ON_GROUND


def test_in_build_rocket_status(repo):
    """Test IN_BUILD status """
    r = repo.add_rocket("Dragon 2")
    
    # change IN_BUILD status
    repo.change_rocket_status(r.id, RocketStatus.IN_BUILD)
    assert repo.get_rocket(r.id).status == RocketStatus.IN_BUILD
    
    # can still assign to mission
    m = repo.add_mission("Test Mission")
    repo.assign_rocket_to_mission(r.id, m.id)
    assert repo.get_rocket(r.id).status == RocketStatus.IN_SPACE  # Changes to IN_SPACE on assignment


def test_mission_status_with_in_build_rockets(repo):
    """test  missions with IN_BUILD rockets behave correctly"""
    r1 = repo.add_rocket("Dragon 1")
    r2 = repo.add_rocket("Dragon 2")
    m = repo.add_mission("Test Mission")
    
    # set one rocket to IN_BUILD
    repo.change_rocket_status(r1.id, RocketStatus.IN_BUILD)
    repo.assign_rocket_to_mission(r1.id, m.id)
    repo.assign_rocket_to_mission(r2.id, m.id)
    # both should be IN_SPACE after assignment
    assert repo.get_rocket(r1.id).status == RocketStatus.IN_SPACE
    assert repo.get_rocket(r2.id).status == RocketStatus.IN_SPACE
    # mission should be IN_PROGRESS (no rockets in repair)
    assert repo.get_mission(m.id).status == MissionStatus.IN_PROGRESS


def test_mission_summary_ordering(repo):
    """tTest  mission summary is ordered by rocket count then name"""
    #create missions with different rocket counts
    m1 = repo.add_mission("Alpha")  # 0 rockets
    m2 = repo.add_mission("Beta")   # 2 rockets  
    m3 = repo.add_mission("Gamma")  # 1 rocket
    r1 = repo.add_rocket("R1")
    r2 = repo.add_rocket("R2")
    r3 = repo.add_rocket("R3")
    repo.assign_rocket_to_mission(r1.id, m2.id)
    repo.assign_rocket_to_mission(r2.id, m2.id)
    repo.assign_rocket_to_mission(r3.id, m3.id)
    
    summary = repo.get_missions_summary()
    assert len(summary) == 3
    #ashould ordered on rocket count
    assert summary[0].name == "Beta"    # 2 rockets
    assert summary[1].name == "Gamma"   # 1 rocket  
    assert summary[2].name == "Alpha"   # 0 rockets