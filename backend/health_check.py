"""
Health Check Module for CloudOps Ninja

This module provides comprehensive health checks for:
- Database connectivity
- External service dependencies
- System resources (CPU and memory)
"""

import psutil
import socket
import requests
from datetime import datetime
from typing import Dict, Any, Tuple


class HealthCheck:
    """Comprehensive health check for CloudOps Ninja"""
    
    def __init__(self, db=None):
        """
        Initialize health checker
        
        Args:
            db: SQLAlchemy database instance
        """
        self.db = db
        self.checks = {}
        
    def check_database(self) -> Tuple[bool, Dict[str, Any]]:
        """Check database connectivity"""
        try:
            if self.db is None:
                return False, {"status": "unhealthy", "error": "Database not configured"}
            
            # Try to execute a simple query using text()
            from sqlalchemy import text
            self.db.session.execute(text("SELECT 1"))
            return True, {
                "status": "healthy",
                "type": "sqlite",
                "message": "Database connection successful"
            }
        except Exception as e:
            return False, {
                "status": "unhealthy",
                "type": "sqlite",
                "error": str(e)
            }
    
    def check_system_resources(self) -> Tuple[bool, Dict[str, Any]]:
        """Check system CPU and memory resources"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            # Try to get disk usage with fallback for psutil Windows issues
            try:
                import platform
                disk_path = 'C:\\' if platform.system() == 'Windows' else '/'
                disk = psutil.disk_usage(disk_path)
                disk_info = {
                    "usage_percent": disk.percent,
                    "total_gb": round(disk.total / 1024 / 1024 / 1024, 2),
                    "free_gb": round(disk.free / 1024 / 1024 / 1024, 2)
                }
            except (SystemError, OSError):
                # Fallback: use shutil.disk_usage or skip disk check on Windows
                try:
                    import shutil
                    stat = shutil.disk_usage('.')
                    disk_info = {
                        "usage_percent": (stat.used / stat.total * 100) if stat.total > 0 else 0,
                        "total_gb": round(stat.total / 1024 / 1024 / 1024, 2),
                        "free_gb": round(stat.free / 1024 / 1024 / 1024, 2)
                    }
                except Exception:
                    # If all fails, provide a placeholder
                    disk_info = {
                        "usage_percent": 0,
                        "total_gb": 0,
                        "free_gb": 0,
                        "note": "Disk metrics unavailable"
                    }
            
            # Determine health based on thresholds
            status = "healthy"
            warnings = []
            
            if cpu_percent > 80:
                status = "degraded"
                warnings.append(f"High CPU usage: {cpu_percent}%")
            
            if memory.percent > 80:
                status = "degraded"
                warnings.append(f"High memory usage: {memory.percent}%")
            
            if disk_info.get("usage_percent", 0) > 85:
                status = "degraded"
                warnings.append(f"High disk usage: {disk_info['usage_percent']}%")
            
            return status == "healthy", {
                "status": status,
                "cpu": {
                    "usage_percent": cpu_percent,
                    "cores": psutil.cpu_count()
                },
                "memory": {
                    "usage_percent": memory.percent,
                    "total_mb": round(memory.total / 1024 / 1024, 2),
                    "available_mb": round(memory.available / 1024 / 1024, 2),
                    "used_mb": round(memory.used / 1024 / 1024, 2)
                },
                "disk": disk_info,
                "warnings": warnings
            }
        except Exception as e:
            return False, {
                "status": "unhealthy",
                "error": str(e)
            }
    
    def check_external_services(self) -> Tuple[bool, Dict[str, Any]]:
        """Check external service dependencies"""
        services = {}
        all_healthy = True
        timeout = 2  # seconds
        
        # Check common service endpoints (DNS resolution and connectivity)
        external_endpoints = [
            ("AWS API", "https://api.aws.amazon.com"),
            ("GCP API", "https://www.googleapis.com"),
            ("DNS Resolution", "8.8.8.8", 53),  # Google DNS
        ]
        
        for check in external_endpoints:
            service_name = check[0]
            
            try:
                if service_name == "DNS Resolution":
                    # Check DNS resolution
                    socket.create_connection((check[1], check[2]), timeout=timeout)
                    services[service_name] = {
                        "status": "healthy",
                        "message": "DNS resolution working"
                    }
                else:
                    # Check HTTP/HTTPS endpoints
                    response = requests.head(check[1], timeout=timeout)
                    services[service_name] = {
                        "status": "healthy",
                        "response_code": response.status_code
                    }
            except requests.Timeout:
                services[service_name] = {
                    "status": "degraded",
                    "error": "Request timeout"
                }
                all_healthy = False
            except requests.ConnectionError:
                services[service_name] = {
                    "status": "degraded",
                    "error": "Connection error (may be offline)"
                }
                all_healthy = False
            except socket.timeout:
                services[service_name] = {
                    "status": "degraded",
                    "error": "Socket timeout"
                }
                all_healthy = False
            except Exception as e:
                services[service_name] = {
                    "status": "degraded",
                    "error": str(e)
                }
                all_healthy = False
        
        return all_healthy, {
            "status": "healthy" if all_healthy else "degraded",
            "services": services
        }
    
    def check_application_status(self) -> Tuple[bool, Dict[str, Any]]:
        """Check application-level status"""
        try:
            from app import db, Deployment, Server
            
            aws_server = db.session.query(Server).filter_by(cloud='aws').first()
            gcp_server = db.session.query(Server).filter_by(cloud='gcp').first()
            total_deployments = db.session.query(Deployment).count()
            
            status = "healthy"
            if not aws_server or not gcp_server:
                status = "degraded"
            
            return status == "healthy", {
                "status": status,
                "aws_server": {
                    "status": aws_server.status if aws_server else "missing",
                    "instances": aws_server.count if aws_server else 0
                },
                "gcp_server": {
                    "status": gcp_server.status if gcp_server else "missing",
                    "instances": gcp_server.count if gcp_server else 0
                },
                "total_deployments": total_deployments
            }
        except Exception as e:
            return False, {
                "status": "unhealthy",
                "error": str(e)
            }
    
    def perform_all_checks(self) -> Dict[str, Any]:
        """Perform all health checks and return comprehensive report"""
        db_healthy, db_info = self.check_database()
        system_healthy, system_info = self.check_system_resources()
        external_healthy, external_info = self.check_external_services()
        app_healthy, app_info = self.check_application_status()
        
        # Determine overall health status
        all_checks = [db_healthy, system_healthy, external_healthy, app_healthy]
        overall_healthy = all(all_checks)
        
        # Count of checks by status
        degraded_count = sum(1 for check in [db_info, system_info, external_info, app_info] 
                            if check.get('status') == 'degraded')
        unhealthy_count = all_checks.count(False) - degraded_count
        
        health_status = "healthy"
        if unhealthy_count > 0:
            health_status = "unhealthy"
        elif degraded_count > 0:
            health_status = "degraded"
        
        return {
            "status": health_status,
            "timestamp": datetime.now().isoformat(),
            "checks": {
                "database": db_info,
                "system_resources": system_info,
                "external_services": external_info,
                "application": app_info
            },
            "summary": {
                "total_checks": 4,
                "healthy": all_checks.count(True),
                "degraded": degraded_count,
                "unhealthy": unhealthy_count
            }
        }


def create_health_checker(app=None):
    """Factory function to create a health checker instance"""
    from app import db
    return HealthCheck(db=db)
