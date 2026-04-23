import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange (setup): snapshot module-level state before each test
    original = copy.deepcopy(activities)
    yield
    # Restore state after each test
    activities.clear()
    activities.update(original)


client = TestClient(app)


def test_get_activities():
    # Arrange
    expected_activities = [
        "Chess Club", "Programming Class", "Gym Class",
        "Basketball Team", "Tennis Club", "Drama Club",
        "Art Studio", "Debate Team", "Science Olympiad",
    ]

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    for name in expected_activities:
        assert name in data


def test_signup_success():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]


def test_signup_activity_not_found():
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404


def test_signup_already_registered():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # already a participant

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400


def test_unregister_success():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # already a participant

    # Act
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]


def test_unregister_activity_not_found():
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404


def test_unregister_not_registered():
    # Arrange
    activity_name = "Chess Club"
    email = "notregistered@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
