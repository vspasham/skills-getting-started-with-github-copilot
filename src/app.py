"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {'Chess Club': {"description": 'Learn strategies and compete in chess tournaments',
             'schedule': 'Fridays, 3:30 PM - 5:00 PM',
             'max_participants': 12,
             'participants': ['michael@mergington.edu', 'daniel@mergington.edu']},
 'Programming Class': {"description": 'Learn programming fundamentals and build software projects',
                   'schedule': 'Tuesdays and Thursdays, 3:30 PM - 4:30 PM',
                   'max_participants': 20,
                   'participants': ['emma@mergington.edu', 'sophia@mergington.edu']},
 'Gym Class': {"description": 'Physical education and sports activities',
            'schedule': 'Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM',
            'max_participants': 30,
            'participants': ['john@mergington.edu', 'olivia@mergington.edu']},
 'Tennis Match': {"description": 'Practice tennis skills and play friendly matches',
               'schedule': 'Fridays, 3:30 PM - 5:00 PM',
               'max_participants': 12,
               'participants': []},
 'Swimming Session': {"description": 'Build swimming techniques and endurance in the school pool',
                  'schedule': 'Fridays, 3:30 PM - 5:00 PM',
                  'max_participants': 12,
                  'participants': []},
 'Watercolor Workshop': {"description": 'Explore watercolor techniques and creative painting',
                    'schedule': 'Fridays, 3:30 PM - 5:00 PM',
                    'max_participants': 12,
                    'participants': []},
 'Theater Improv': {"description": 'Develop acting confidence through improv games and scenes',
                'schedule': 'Fridays, 3:30 PM - 5:00 PM',
                'max_participants': 12,
                'participants': []},
 'Math Puzzle Club': {"description": 'Solve logic problems, brainteasers, and math challenges',
                  'schedule': 'Fridays, 3:30 PM - 5:00 PM',
                  'max_participants': 12,
                  'participants': []},
 'Soccer Practice': {"description": 'Improve teamwork, drills, and match play in soccer',
                 'schedule': 'Mondays and Wednesdays, 3:30 PM - 5:00 PM',
                 'max_participants': 18,
                 'participants': []},
 'Basketball Training': {"description": 'Develop basketball fundamentals and scrimmage skills',
                    'schedule': 'Tuesdays, 3:30 PM - 5:00 PM',
                    'max_participants': 15,
                    'participants': []},
 'Digital Photography': {"description": 'Learn composition, lighting, and photo storytelling',
                    'schedule': 'Thursdays, 3:30 PM - 5:00 PM',
                    'max_participants': 14,
                    'participants': []},
 'Sculpture Studio': {"description": 'Create 3D artworks using clay and mixed materials',
                  'schedule': 'Wednesdays, 3:30 PM - 5:00 PM',
                  'max_participants': 10,
                  'participants': []},
 'Debate Team': {"description": 'Practice argumentation, public speaking, and critical thinking',
              'schedule': 'Mondays, 3:30 PM - 5:00 PM',
              'max_participants': 16,
              'participants': []},
 'Science Olympiad': {"description": 'Prepare for science competitions through team problem-solving',
                  'schedule': 'Thursdays, 3:30 PM - 5:00 PM',
                  'max_participants': 16,
                  'participants': []},
 'Robotics Club': {"description": 'Design, build, and program robots for challenges',
               'schedule': 'Tuesdays, 4:00 PM - 5:30 PM',
               'max_participants': 14,
               'participants': []},
 'Creative Writing': {"description": 'Develop storytelling, poetry, and editing skills',
                  'schedule': 'Wednesdays, 3:30 PM - 5:00 PM',
                  'max_participants': 12,
                  'participants': []},
 'Music Ensemble': {"description": 'Rehearse and perform as a collaborative school ensemble',
                'schedule': 'Thursdays, 4:00 PM - 5:30 PM',
                'max_participants': 20,
                'participants': []},
 'Environmental Club': {"description": 'Lead sustainability projects and campus clean-up efforts',
                    'schedule': 'Fridays, 2:30 PM - 4:00 PM',
                    'max_participants': 18,
                    'participants': []}}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/participants")
def cancel_activity_registration(activity_name: str, email: str):
    """Cancel a student's activity registration"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    # Validate student is currently signed up
    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Student not signed up for this activity")

    activity["participants"].remove(email)
    return {"message": f"Cancelled registration for {email} from {activity_name}"}
