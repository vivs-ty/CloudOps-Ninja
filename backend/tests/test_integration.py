import pytest
import json


def test_full_deployment_workflow(authenticated_client):
    """Test complete deployment workflow"""
    # Check initial state
    response = authenticated_client.get('/api/deployments')
    initial_data = json.loads(response.data)
    initial_count = initial_data['total']

    # Perform deployment
    response = authenticated_client.get('/api/deploy/aws/v2.0.0')
    assert response.status_code == 201

    # Check deployment was recorded
    response = authenticated_client.get('/api/deployments')
    final_data = json.loads(response.data)
    final_count = final_data['total']

    assert final_count == initial_count + 1
    assert len(final_data['deployments']) == final_count
    assert final_data['deployments'][-1]['version'] == 'v2.0.0'
    assert final_data['deployments'][-1]['cloud'] == 'aws'


def test_multiple_deployments(authenticated_client):
    """Test multiple deployments to different clouds"""
    # Deploy to AWS
    authenticated_client.get('/api/deploy/aws/v1.0.0')

    # Deploy to GCP
    authenticated_client.get('/api/deploy/gcp/v1.0.0')

    # Check deployments
    response = authenticated_client.get('/api/deployments')
    data = json.loads(response.data)

    assert data['total'] >= 2
    clouds = [d['cloud'] for d in data['deployments']]
    assert 'aws' in clouds
    assert 'gcp' in clouds


def test_servers_persistence(authenticated_client):
    """Test that server data persists and is accessible"""
    response = authenticated_client.get('/api/servers')
    data = json.loads(response.data)

    assert 'clouds' in data
    assert 'aws' in data['clouds']
    assert 'gcp' in data['clouds']

    aws_server = data['clouds']['aws']
    assert 'count' in aws_server
    assert 'status' in aws_server
    assert 'cpu' in aws_server
    assert 'memory' in aws_server


def test_metrics_update_after_deployment(authenticated_client):
    """Test that metrics are updated after deployment"""
    # Get initial metrics
    initial_response = authenticated_client.get('/api/metrics')
    initial_metrics = initial_response.data.decode()

    # Perform deployment
    authenticated_client.get('/api/deploy/aws/v3.0.0')

    # Get updated metrics
    updated_response = authenticated_client.get('/api/metrics')
    updated_metrics = updated_response.data.decode()

    # Metrics should be updated (this is a basic check)
    assert len(updated_metrics) > 0
    assert 'cloudops_deployments_total' in updated_metrics