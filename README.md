# six_test
An in memory Python library excercise for managing SpaceX style rockets .

Rocket Ops: Add, update status, assign/unassign to missions
Mission Ops: Create, assign rockets, auto-update status
Business Logic: Enforces single rocket assignment, mission lifecycle rules
Status Tracking: Reflects rocket repairs and mission progress

## Installation
```bash
# Install in development mode
pip install -e .```

## Usage
```python
from src.dragon_repo import SpaceXRepository
repo = SpaceXRepository()
#add rockets and missions
rocket = repo.add_rocket("Dragon 1")
mission = repo.add_mission("Mars Mission")
#assign rocket to mission
repo.assign_rocket_to_mission(rocket.id, mission.id)
#status
print(f"Rocket status: {rocket.status}")  
print(f"Mission status: {mission.status}")  
repo.change_rocket_status(rocket.id, RocketStatus.IN_REPAIR)
summary = repo.get_missions_summary()
```

### Running Tests
```bash
pytest
```

## Assumptions
1. **Rocket names are not unique**
2. **Mission names are not unique**
3. **Status transitions are automatic**
4. **In-memory only**: data is lost on restart
5. **Single-threaded**: No concurrency

### Rocket Statuses
- **On ground**: Initial status
- **In space**: Assigned
- **In repair**: Due for maintenance
- **In build**: Under construction

### Mission Statuses
- **Scheduled**: Initial status
- **Pending**: Rockets assigned
- **In progress**: Rockets assigned
- **Ended**: Final status

## Business Rules
1. **One rocket per mission**
2. **No assignments to ended missions**
3. **Mission ending requires zero rockets**
4. **Automatic status transitions**
5. **Mission status auto-update**

### Architecture
- **In-memory storage**, **Repository pattern**, **Type safety**, **Exception handling**
