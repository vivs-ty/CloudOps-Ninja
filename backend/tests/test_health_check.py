"""
Tests for Health Check Module
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from health_check import HealthCheck


class TestHealthCheckDatabase:
    """Test database connectivity checks"""
    
    def test_database_check_success(self):
        """Test successful database connection check"""
        # Mock the database
        mock_db = Mock()
        mock_db.session = Mock()
        mock_db.session.execute = Mock()
        
        health_checker = HealthCheck(db=mock_db)
        result, info = health_checker.check_database()
        
        assert result is True
        assert info['status'] == 'healthy'
        assert info['type'] == 'sqlite'
    
    def test_database_check_failure(self):
        """Test failed database connection check"""
        # Mock the database with an error
        mock_db = Mock()
        mock_db.session = Mock()
        mock_db.session.execute = Mock(side_effect=Exception("Connection failed"))
        
        health_checker = HealthCheck(db=mock_db)
        result, info = health_checker.check_database()
        
        assert result is False
        assert info['status'] == 'unhealthy'
        assert 'error' in info
    
    def test_database_check_no_db_configured(self):
        """Test database check when no database is configured"""
        health_checker = HealthCheck(db=None)
        result, info = health_checker.check_database()
        
        assert result is False
        assert info['status'] == 'unhealthy'


class TestHealthCheckSystemResources:
    """Test system resource checks"""
    
    @patch('psutil.cpu_percent')
    @patch('psutil.cpu_count')
    @patch('psutil.virtual_memory')
    @patch('psutil.disk_usage')
    def test_system_resources_healthy(self, mock_disk, mock_memory, mock_cpu_count, mock_cpu_percent):
        """Test healthy system resources"""
        mock_cpu_percent.return_value = 30
        mock_cpu_count.return_value = 4
        
        mock_mem = Mock()
        mock_mem.percent = 40
        mock_mem.total = 16 * 1024 * 1024 * 1024  # 16GB
        mock_mem.available = 8 * 1024 * 1024 * 1024
        mock_mem.used = 8 * 1024 * 1024 * 1024
        mock_memory.return_value = mock_mem
        
        mock_disk_obj = Mock()
        mock_disk_obj.percent = 60
        mock_disk_obj.total = 250 * 1024 * 1024 * 1024  # 250GB
        mock_disk_obj.free = 100 * 1024 * 1024 * 1024
        mock_disk.return_value = mock_disk_obj
        
        health_checker = HealthCheck()
        result, info = health_checker.check_system_resources()
        
        assert result is True
        assert info['status'] == 'healthy'
        assert 'cpu' in info
        assert 'memory' in info
        assert 'disk' in info
    
    @patch('psutil.cpu_percent')
    @patch('psutil.cpu_count')
    @patch('psutil.virtual_memory')
    @patch('psutil.disk_usage')
    def test_system_resources_high_cpu(self, mock_disk, mock_memory, mock_cpu_count, mock_cpu_percent):
        """Test high CPU usage alert"""
        mock_cpu_percent.return_value = 90  # High CPU
        mock_cpu_count.return_value = 4
        
        mock_mem = Mock()
        mock_mem.percent = 40
        mock_mem.total = 16 * 1024 * 1024 * 1024
        mock_mem.available = 8 * 1024 * 1024 * 1024
        mock_mem.used = 8 * 1024 * 1024 * 1024
        mock_memory.return_value = mock_mem
        
        mock_disk_obj = Mock()
        mock_disk_obj.percent = 60
        mock_disk_obj.total = 250 * 1024 * 1024 * 1024
        mock_disk_obj.free = 100 * 1024 * 1024 * 1024
        mock_disk.return_value = mock_disk_obj
        
        health_checker = HealthCheck()
        result, info = health_checker.check_system_resources()
        
        assert info['status'] == 'degraded'
        assert len(info['warnings']) > 0


class TestHealthCheckExternalServices:
    """Test external service dependency checks"""
    
    @patch('socket.create_connection')
    @patch('requests.head')
    def test_external_services_healthy(self, mock_head, mock_socket):
        """Test healthy external services"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_head.return_value = mock_response
        mock_socket.return_value = True
        
        health_checker = HealthCheck()
        result, info = health_checker.check_external_services()
        
        assert 'services' in info
        for service, status in info['services'].items():
            assert 'status' in status
    
    @patch('socket.create_connection')
    @patch('requests.head')
    def test_external_services_connection_error(self, mock_head, mock_socket):
        """Test connection errors in external services"""
        import requests
        mock_head.side_effect = requests.ConnectionError("Network error")
        mock_socket.side_effect = Exception("Connection failed")
        
        health_checker = HealthCheck()
        result, info = health_checker.check_external_services()
        
        assert result is False
        assert info['status'] == 'degraded'


class TestHealthCheckFullReport:
    """Test full health check reports"""
    
    @patch('psutil.cpu_percent')
    @patch('psutil.cpu_count')
    @patch('psutil.virtual_memory')
    @patch('psutil.disk_usage')
    @patch('socket.create_connection')
    @patch('requests.head')
    def test_full_health_check_report(self, mock_head, mock_socket, mock_disk, mock_memory, 
                                       mock_cpu_count, mock_cpu_percent):
        """Test full health check report generation"""
        # Setup mocks
        mock_cpu_percent.return_value = 30
        mock_cpu_count.return_value = 4
        
        mock_mem = Mock()
        mock_mem.percent = 40
        mock_mem.total = 16 * 1024 * 1024 * 1024
        mock_mem.available = 8 * 1024 * 1024 * 1024
        mock_mem.used = 8 * 1024 * 1024 * 1024
        mock_memory.return_value = mock_mem
        
        mock_disk_obj = Mock()
        mock_disk_obj.percent = 60
        mock_disk_obj.total = 250 * 1024 * 1024 * 1024
        mock_disk_obj.free = 100 * 1024 * 1024 * 1024
        mock_disk.return_value = mock_disk_obj
        
        # Create mock database
        mock_db = Mock()
        mock_db.session = Mock()
        mock_db.session.execute = Mock()
        
        health_checker = HealthCheck(db=mock_db)
        report = health_checker.perform_all_checks()
        
        # Verify report structure
        assert 'status' in report
        assert 'timestamp' in report
        assert 'checks' in report
        assert 'summary' in report
        
        # Verify checks
        assert 'database' in report['checks']
        assert 'system_resources' in report['checks']
        assert 'external_services' in report['checks']
        assert 'application' in report['checks']
        
        # Verify summary
        assert report['summary']['total_checks'] == 4
        assert 'healthy' in report['summary']
        assert 'degraded' in report['summary']
        assert 'unhealthy' in report['summary']
