# Atlas Documentation

Welcome to the Atlas documentation. This comprehensive guide covers all aspects of the Atlas task management and automation system.

## Quick Start

New to Atlas? Start here:
1. [README](../README.md) - Basic setup and usage
2. [System Specifications](system-specs.md) - Technical overview and architecture
3. [Task Configuration](task-configuration.md) - How to configure and manage tasks

## Documentation Sections

### Core Documentation

| Document | Description | Audience |
|----------|-------------|-----------|
| [System Specifications](system-specs.md) | Technical architecture, MVP features, deployment considerations | Developers, System Architects |
| [Task Configuration Guide](task-configuration.md) | Complete guide to configuring tasks, condition types, and actions | Users, Administrators |
| [Logging Guide](logging.md) | Logging system, debug mode, troubleshooting | Developers, Operations |

### Configuration References

- **Task Types**: Monitoring, maintenance, integration, business logic
- **Condition Types**: Time-based, interval, loop, cron, threshold
- **Actions**: Built-in actions and custom implementations
- **Logging Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL

## Atlas Features by Use Case

### API Integration Management
Atlas helps manage API integrations with automated tasks for:
- Authentication token refresh
- Health monitoring and availability checks  
- Data synchronization between systems
- Rate limit management and retry logic

**Relevant Documentation:**
- [Task Configuration - API Integration Scenario](task-configuration.md#api-integration-scenario)
- [System Specs - Integration Tasks](system-specs.md#integration-tasks)

### System Monitoring and Maintenance
Automated system management tasks including:
- Resource monitoring (CPU, memory, disk)
- Log rotation and cleanup
- Database maintenance and optimization
- Health checks and alerting

**Relevant Documentation:**
- [Task Configuration - System Maintenance Scenario](task-configuration.md#system-maintenance-scenario)
- [Logging Guide - Production Best Practices](logging.md#production-logging-best-practices)

### Development and Testing
Development workflow support with:
- Debug mode for verbose logging
- Test data generation and cleanup
- Configuration validation
- Interactive service management

**Relevant Documentation:**
- [Logging Guide - Debug Mode](logging.md#debug-mode-vs-normal-mode)
- [Task Configuration - Development Scenario](task-configuration.md#development-and-testing-scenario)

## Condition Types Deep Dive

Atlas supports multiple execution patterns to handle different automation needs:

### Time-based Execution
Execute tasks at specific times of day (e.g., daily reports, maintenance windows):
```json
{
  "condition_type": "time",
  "condition_value": 480  // 8:00 AM (480 minutes since midnight)
}
```

### Interval-based Execution  
Execute tasks every N seconds (e.g., health checks, monitoring):
```json
{
  "condition_type": "interval", 
  "condition_value": 300  // Every 5 minutes
}
```

### Loop-based Execution
Execute tasks every application cycle (e.g., continuous monitoring):
```json
{
  "condition_type": "loop",
  "condition_value": 1  // Every loop iteration (~10 seconds)
}
```

### Future Condition Types (Roadmap)

#### Cron-style Scheduling
```json
{
  "condition_type": "cron",
  "condition_value": "0 2 * * 1"  // 2:00 AM every Monday
}
```

#### Threshold-based Triggers
```json
{
  "condition_type": "threshold",
  "condition_value": {
    "metric": "cpu_usage",
    "operator": ">", 
    "value": 80,
    "duration": 300
  }
}
```

#### Event-driven Execution
```json
{
  "condition_type": "event",
  "condition_value": {
    "event_type": "file_created",
    "path": "/data/incoming/",
    "pattern": "*.json"
  }
}
```

## Configuration Examples by Industry

### E-commerce Platform
```json
{
  "tasks": [
    {
      "name": "Inventory Sync",
      "action": "sync_inventory_data",
      "condition_type": "interval",
      "condition_value": 900
    },
    {
      "name": "Price Updates",
      "action": "update_pricing",
      "condition_type": "time", 
      "condition_value": 360
    },
    {
      "name": "Order Processing Health",
      "action": "check_order_system",
      "condition_type": "interval",
      "condition_value": 60
    }
  ]
}
```

### Financial Services
```json
{
  "tasks": [
    {
      "name": "Market Data Feed",
      "action": "sync_market_data",
      "condition_type": "loop",
      "condition_value": 1
    },
    {
      "name": "Risk Calculations", 
      "action": "calculate_risk_metrics",
      "condition_type": "time",
      "condition_value": 540
    },
    {
      "name": "Compliance Check",
      "action": "run_compliance_audit",
      "condition_type": "time",
      "condition_value": 120
    }
  ]
}
```

### Healthcare System
```json
{
  "tasks": [
    {
      "name": "Patient Data Sync",
      "action": "sync_patient_records", 
      "condition_type": "interval",
      "condition_value": 1800
    },
    {
      "name": "Backup Critical Data",
      "action": "backup_patient_data",
      "condition_type": "time",
      "condition_value": 180
    },
    {
      "name": "System Health Monitor",
      "action": "monitor_ehr_system",
      "condition_type": "interval", 
      "condition_value": 300
    }
  ]
}
```