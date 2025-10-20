# six_test
An in memory Python library excercise for managing SpaceX style rockets .

Rocket Ops: Add, update status, assign/unassign to missions
Mission Ops: Create, assign rockets, auto-update status
Business Logic: Enforces single rocket assignment, mission lifecycle rules
Status Tracking: Reflects rocket repairs and mission progress

Usage example
<pre>
from src.dragon_repo import SpaceXRepository
repo = SpaceXRepository()
rocket = repo.add_rocket("Dragon 1")
mission = repo.add_mission("Mars Mission") </pre>

Business Rules
One rocket per mission
No rocket assignments to ended missions
Mission status updates automatically
Missions can't end while rockets are assigned
