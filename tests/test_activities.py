def test_get_activities(client):
    """Test retrieving all activities."""
    # Arrange
    # (no setup needed, activities exist by default)
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_activity_has_required_fields(client):
    """Test that activities have required fields."""
    # Arrange
    # (no setup needed)
    
    # Act
    response = client.get("/activities")
    activity = response.json()["Chess Club"]
    
    # Assert
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity


def test_signup_new_student(client):
    """Test signing up a new student."""
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    assert email in response.json()["message"]


def test_signup_duplicate_fails(client):
    """Test that duplicate signup fails."""
    # Arrange
    email = "michael@mergington.edu"  # already registered in Chess Club
    activity = "Chess Club"
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_nonexistent_activity_fails(client):
    """Test signup fails for nonexistent activity."""
    # Arrange
    email = "alice@mergington.edu"
    activity = "Fake Activity"
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_unregister_participant(client):
    """Test unregistering a participant."""
    # Arrange
    email = "michael@mergington.edu"
    activity = "Chess Club"
    
    # Act
    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    assert email in response.json()["message"]


def test_unregister_nonexistent_participant_fails(client):
    """Test unregister fails for nonexistent participant."""
    # Arrange
    email = "notregistered@mergington.edu"
    activity = "Chess Club"
    
    # Act
    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "not registered" in response.json()["detail"].lower()


def test_root_redirects(client):
    """Test root redirects to static files."""
    # Arrange
    # (no setup needed)
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307
    assert "/static/index.html" in response.headers["location"]
