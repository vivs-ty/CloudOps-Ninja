import pytest
import json


def test_home_redirect_unauthenticated(client):
    """Test home page redirects when not authenticated"""
    response = client.get('/')
    assert response.status_code == 302  # Redirect to login


def test_login_page(client):
    """Test login page loads"""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data


def test_login_success(client):
    """Test successful login"""
    response = client.post('/login', data={'username': 'admin', 'password': 'password'}, follow_redirects=False)
    assert response.status_code == 302  # Redirect to home


def test_api_status(client):
    """Test status API endpoint"""
    response = client.get('/api/status')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'status' in data
    assert data['status'] == 'healthy'


def test_api_servers_authenticated(authenticated_client):
    """Test servers API with authentication"""
    response = authenticated_client.get('/api/servers')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'clouds' in data
    assert 'aws' in data['clouds']
    assert 'gcp' in data['clouds']


def test_api_deployments_authenticated(authenticated_client):
    """Test deployments API with authentication"""
    response = authenticated_client.get('/api/deployments')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'deployments' in data
    assert 'total' in data


def test_deploy_authenticated(authenticated_client):
    """Test deployment creation with authentication"""
    response = authenticated_client.get('/api/deploy/aws/v1.0.0')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'message' in data
    assert 'deployment' in data


def test_deploy_unauthenticated(client):
    """Test deployment creation without authentication redirects"""
    response = client.get('/api/deploy/aws/v1.0.0')
    assert response.status_code == 302  # Redirect to login


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/api/status')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'status' in data


def test_metrics_endpoint(client):
    """Test Prometheus metrics endpoint"""
    response = client.get('/metrics')
    assert response.status_code == 200
    assert b'cloudops_deployments_total' in response.data


def test_api_metrics_authenticated(authenticated_client):
    """Test API metrics endpoint with authentication"""
    response = authenticated_client.get('/api/metrics')
    assert response.status_code == 200
    assert b'cloudops_deployments_total' in response.data


def test_logout(authenticated_client):
    """Test logout functionality"""
    response = authenticated_client.get('/logout')
    assert response.status_code == 302  # Redirect to login


def test_api_health_check(client):
    """Test comprehensive health check endpoint"""
    response = client.get('/api/health')
    assert response.status_code in [200, 503]
    data = json.loads(response.data)
    
    # Verify health check structure
    assert 'status' in data
    assert data['status'] in ['healthy', 'degraded', 'unhealthy']
    assert 'timestamp' in data
    assert 'checks' in data
    assert 'summary' in data


def test_api_health_check_includes_database_check(client):
    """Test health check includes database connectivity check"""
    response = client.get('/api/health')
    assert response.status_code in [200, 503]
    data = json.loads(response.data)
    
    assert 'database' in data['checks']
    assert 'status' in data['checks']['database']


def test_api_health_check_includes_system_resources(client):
    """Test health check includes system resources check"""
    response = client.get('/api/health')
    assert response.status_code in [200, 503]
    data = json.loads(response.data)
    
    assert 'system_resources' in data['checks']
    system_check = data['checks']['system_resources']
    assert 'cpu' in system_check
    assert 'memory' in system_check
    assert 'disk' in system_check
    assert 'usage_percent' in system_check['cpu']
    assert 'usage_percent' in system_check['memory']
    assert 'usage_percent' in system_check['disk']


def test_api_health_check_includes_external_services(client):
    """Test health check includes external services check"""
    response = client.get('/api/health')
    assert response.status_code in [200, 503]
    data = json.loads(response.data)
    
    assert 'external_services' in data['checks']
    assert 'services' in data['checks']['external_services']


def test_api_health_check_includes_application_status(client):
    """Test health check includes application status check"""
    response = client.get('/api/health')
    assert response.status_code in [200, 503]
    data = json.loads(response.data)
    
    assert 'application' in data['checks']
    assert 'aws_server' in data['checks']['application']
    assert 'gcp_server' in data['checks']['application']


def test_api_health_check_summary(client):
    """Test health check includes summary statistics"""
    response = client.get('/api/health')
    assert response.status_code in [200, 503]
    data = json.loads(response.data)
    
    summary = data['summary']
    assert 'total_checks' in summary
    assert 'healthy' in summary
    assert summary['total_checks'] == 4  # Database, system, external, application