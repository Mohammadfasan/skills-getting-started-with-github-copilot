from src import app as app_module


def test_get_activities_returns_known_activity(client):
    response = client.get("/activities")

    assert response.status_code == 200
    assert "Chess Club" in response.json()
    assert response.json()["Chess Club"]["max_participants"] == 12


def test_signup_adds_participant(client):
    email = "student@example.com"

    response = client.post("/activities/Art Club/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Art Club"}
    assert email in app_module.activities["Art Club"]["participants"]


def test_duplicate_signup_is_rejected(client):
    activity_name = "Chess Club"
    email = "student@example.com"

    first_response = client.post(
        f"/activities/{activity_name}/signup", params={"email": email}
    )
    duplicate_response = client.post(
        f"/activities/{activity_name}/signup", params={"email": email}
    )

    assert first_response.status_code == 200
    assert duplicate_response.status_code == 400
    assert duplicate_response.json()["detail"] == "Student already signed up for this activity"
    assert app_module.activities[activity_name]["participants"].count(email) == 1


def test_signup_for_unknown_activity_returns_not_found(client):
    response = client.post(
        "/activities/Unknown Club/signup", params={"email": "student@example.com"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_removes_participant(client):
    activity_name = "Art Club"
    email = "student@example.com"
    app_module.activities[activity_name]["participants"].append(email)

    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity_name}"}
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregistering_unknown_participant_returns_not_found(client):
    response = client.delete(
        "/activities/Art Club/participants/student@example.com"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
