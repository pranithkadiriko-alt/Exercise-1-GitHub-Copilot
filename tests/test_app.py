import pytest
from fastapi.testclient import TestClient

class TestActivitiesAPI:
    """Test suite for activities API using AAA pattern."""

    def test_get_activities_success(self, client: TestClient):
        # Arrange: No special setup needed

        # Act: Make GET request to /activities
        response = client.get("/activities")

        # Assert: Verify response structure and data
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "Chess Club" in data
        assert "participants" in data["Chess Club"]

    def test_signup_for_activity_success(self, client: TestClient):
        # Arrange: Prepare test data
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act: Perform signup
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # Assert: Check success response and state change
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == f"Signed up {email} for {activity_name}"

        # Verify participant was added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity_name]["participants"]

    def test_signup_for_activity_already_signed_up(self, client: TestClient):
        # Arrange: Use existing participant
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up

        # Act: Attempt duplicate signup
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # Assert: Verify error response
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "Student already signed up for this activity"

    def test_signup_for_activity_not_found(self, client: TestClient):
        # Arrange: Use non-existent activity
        activity_name = "NonExistentActivity"
        email = "student@mergington.edu"

        # Act: Attempt signup
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # Assert: Verify 404 response
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Activity not found"

    def test_remove_participant_success(self, client: TestClient):
        # Arrange: Ensure participant exists
        activity_name = "Programming Class"
        email = "emma@mergington.edu"  # Already in participants

        # Act: Remove participant
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        # Assert: Check success and state change
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == f"Removed {email} from {activity_name}"

        # Verify participant was removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email not in activities[activity_name]["participants"]

    def test_remove_participant_not_found_in_activity(self, client: TestClient):
        # Arrange: Use email not in activity
        activity_name = "Programming Class"
        email = "notparticipant@mergington.edu"

        # Act: Attempt removal
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        # Assert: Verify 404 response
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Participant not found in this activity"

    def test_remove_participant_activity_not_found(self, client: TestClient):
        # Arrange: Use non-existent activity
        activity_name = "NonExistentActivity"
        email = "student@mergington.edu"

        # Act: Attempt removal
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        # Assert: Verify 404 response
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Activity not found"