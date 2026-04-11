# RDS Database Module
# Creates a managed PostgreSQL/MySQL database instance

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Database Subnet Group
resource "aws_db_subnet_group" "main" {
  name        = "${var.environment}-${var.project_name}-db-subnet-group"
  description = "Database subnet group for ${var.project_name}"
  subnet_ids  = var.subnet_ids

  tags = {
    Name        = "${var.environment}-${var.project_name}-db-subnet-group"
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "terraform"
  }
}

# RDS Instance
resource "aws_db_instance" "main" {
  identifier = "${var.environment}-${var.project_name}-db"

  # Engine Configuration
  engine         = var.engine
  engine_version = var.engine_version
  instance_class = var.instance_class

  # Database Configuration
  db_name  = var.database_name
  username = var.database_username
  password = var.database_password

  # Storage Configuration
  allocated_storage     = var.allocated_storage
  max_allocated_storage = var.max_allocated_storage
  storage_type          = var.storage_type
  storage_encrypted     = var.storage_encrypted
  kms_key_id           = var.kms_key_id

  # Network Configuration
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = var.vpc_security_group_ids
  publicly_accessible    = var.publicly_accessible
  port                   = var.database_port

  # Maintenance & Backup
  maintenance_window              = var.maintenance_window
  backup_window                  = var.backup_window
  backup_retention_period        = var.backup_retention_period
  copy_tags_to_snapshot          = var.copy_tags_to_snapshot
  delete_automated_backups       = var.delete_automated_backups
  deletion_protection            = var.deletion_protection
  skip_final_snapshot           = var.skip_final_snapshot
  final_snapshot_identifier     = var.final_snapshot_identifier

  # Monitoring & Performance
  monitoring_interval = var.monitoring_interval
  monitoring_role_arn = var.monitoring_role_arn
  performance_insights_enabled          = var.performance_insights_enabled
  performance_insights_kms_key_id      = var.performance_insights_kms_key_id
  performance_insights_retention_period = var.performance_insights_retention_period

  # Parameter Group
  parameter_group_name = var.parameter_group_name != "" ? var.parameter_group_name : aws_db_parameter_group.main[0].name
  option_group_name    = var.option_group_name != "" ? var.option_group_name : aws_db_option_group.main[0].name

  # Auto Minor Version Upgrade
  auto_minor_version_upgrade = var.auto_minor_version_upgrade

  # Multi-AZ
  multi_az = var.multi_az

  # License Model (for Oracle)
  license_model = var.license_model

  tags = {
    Name        = "${var.environment}-${var.project_name}-db"
    Environment = var.environment
    Project     = var.project_name
    Engine      = var.engine
    ManagedBy   = "terraform"
  }

  depends_on = [
    aws_db_subnet_group.main,
    aws_db_parameter_group.main,
    aws_db_option_group.main
  ]

  lifecycle {
    ignore_changes = [
      password,  # Ignore password changes to avoid recreation
    ]
  }
}

# DB Parameter Group (Conditional)
resource "aws_db_parameter_group" "main" {
  count = var.parameter_group_name == "" ? 1 : 0

  family = var.parameter_group_family
  name   = "${var.environment}-${var.project_name}-db-parameter-group"

  dynamic "parameter" {
    for_each = var.db_parameters
    content {
      name  = parameter.value.name
      value = parameter.value.value
      apply_method = lookup(parameter.value, "apply_method", "immediate")
    }
  }

  tags = {
    Name        = "${var.environment}-${var.project_name}-db-parameter-group"
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "terraform"
  }
}

# DB Option Group (Conditional)
resource "aws_db_option_group" "main" {
  count = var.option_group_name == "" && var.engine == "mysql" ? 1 : 0

  engine         = var.engine
  engine_version = var.engine_version
  name           = "${var.environment}-${var.project_name}-db-option-group"

  dynamic "option" {
    for_each = var.db_options
    content {
      option_name = option.value.option_name
      dynamic "option_settings" {
        for_each = lookup(option.value, "option_settings", [])
        content {
          name  = option_settings.value.name
          value = option_settings.value.value
        }
      }
    }
  }

  tags = {
    Name        = "${var.environment}-${var.project_name}-db-option-group"
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "terraform"
  }
}

# CloudWatch Alarms for RDS (Optional)
resource "aws_cloudwatch_metric_alarm" "database_cpu_utilization" {
  count = var.enable_cloudwatch_alarms ? 1 : 0

  alarm_name          = "${var.environment}-${var.project_name}-db-cpu-utilization"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/RDS"
  period              = "300"
  statistic           = "Average"
  threshold           = var.cpu_utilization_threshold
  alarm_description   = "This metric monitors RDS CPU utilization"
  alarm_actions       = var.alarm_actions

  dimensions = {
    DBInstanceIdentifier = aws_db_instance.main.identifier
  }

  tags = {
    Name        = "${var.environment}-${var.project_name}-db-cpu-alarm"
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "terraform"
  }
}

resource "aws_cloudwatch_metric_alarm" "database_free_storage_space" {
  count = var.enable_cloudwatch_alarms ? 1 : 0

  alarm_name          = "${var.environment}-${var.project_name}-db-free-storage"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "FreeStorageSpace"
  namespace           = "AWS/RDS"
  period              = "300"
  statistic           = "Average"
  threshold           = var.free_storage_threshold
  alarm_description   = "This metric monitors RDS free storage space"
  alarm_actions       = var.alarm_actions

  dimensions = {
    DBInstanceIdentifier = aws_db_instance.main.identifier
  }

  tags = {
    Name        = "${var.environment}-${var.project_name}-db-storage-alarm"
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "terraform"
  }
}