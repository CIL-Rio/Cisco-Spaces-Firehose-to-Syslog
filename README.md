# Cisco Spaces Firehose to Syslog

This project processes events from Cisco Spaces FirehoseAPI and forwards them to a syslog server. It includes filtering capabilities to reduce message size and focuses on DEVICE_LOCATION_UPDATE events.

## Features

- Real-time DNA Spaces FirehoseAPI event streaming and processing
- Filters out "KEEP_ALIVE" events
- Optional event filtering to reduce message size
- Forwards events to syslog server
- Docker containerized solution

## Prerequisites

Before you begin, ensure you have:
- Docker and Docker Compose installed
- Cisco Spaces API key
- Syslog server (OpenObserve included in docker-compose)

## Configuration

The application is configured through environment variables in docker-compose.yml:

- `X_API_KEY`: Your DNA Spaces API key
- `SYSLOG_HOST`: Syslog server hostname (default: openobserve)
- `SYSLOG_PORT`: Syslog server port (default: 5514)
- `ENABLE_FILTERING`: Enable/disable event filtering (true/false)

## Running the Application

1. Clone the repository
2. Update the X_API_KEY in docker-compose.yml
3. Start the application:

```bash
docker-compose up --build
```

## Event Filtering

When `ENABLE_FILTERING=true`, the application will only forward these fields:
- recordUid
- recordTimestamp
- eventType
- deviceLocationUpdate
  - device (deviceId, userId, mobile, email, macAddress)
  - openRoamingUserId
  - ssid
  - rawUserId
  - ipv4
  - ipv6

Set `ENABLE_FILTERING=false` in docker-compose.yml to receive complete events.

