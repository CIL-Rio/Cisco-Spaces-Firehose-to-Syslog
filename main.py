import requests
import json
import os
import logging
import logging.handlers

# Read environment variables
API_KEY = os.getenv('X_API_KEY')
SYSLOG_HOST = os.getenv('SYSLOG_HOST', 'localhost')
SYSLOG_PORT = int(os.getenv('SYSLOG_PORT', '514'))
ENABLE_FILTERING = os.getenv('ENABLE_FILTERING', 'true').lower() == 'true'

# Configure syslog logger
logger = logging.getLogger('DNASpaces')
logger.setLevel(logging.INFO)
handler = logging.handlers.SysLogHandler(address=(SYSLOG_HOST, SYSLOG_PORT))
logger.addHandler(handler)

def stream():
    '''
    Opens a new HTTP session that we can use to terminate firehose onto
    '''
    sess = requests.Session()
    sess.headers = {'X-API-Key': API_KEY}
    stream = sess.get(
        f'https://partners.dnaspaces.io/api/partners/v1/firehose/events', stream=True)  

    # Jumps through every new event we have through firehose
    print("Starting Stream")
    
    try:
        for line in stream.iter_lines():
            if line:
                print(line)
                # decodes payload into useable format
                decoded_line = line.decode('utf-8')
                event = json.loads(decoded_line)

                # Extracts the event type
                eventType = event['eventType']

                # Only process DEVICE_PRESENCE events
                if eventType == "KEEP_ALIVE":
                    print(".")
                    continue
                elif eventType == "DEVICE_LOCATION_UPDATE":
                    syslog_handler(event)
                else:
                    print(f"Skipping event type: {eventType}")
           

    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        pass
    
    print("Closing Stream")
    stream.close()
    sess.close()
    
def filter_event(event):
    """Filter event to keep only specified fields"""
    if not ENABLE_FILTERING:
        return event
        
    filtered_event = {
        'recordUid': event.get('recordUid'),
        'recordTimestamp': event.get('recordTimestamp'),
        'eventType': event.get('eventType')
    }
    
    if 'deviceLocationUpdate' in event:
        device_data = event['deviceLocationUpdate'].get('device', {})
        filtered_device = {
            'deviceId': device_data.get('deviceId'),
            'userId': device_data.get('userId'),
            'mobile': device_data.get('mobile'),
            'email': device_data.get('email'),
            'macAddress': device_data.get('macAddress')
        }
        
        filtered_event['deviceLocationUpdate'] = {
            'device': filtered_device,
            'openRoamingUserId': event['deviceLocationUpdate'].get('openRoamingUserId'),
            'ssid': event['deviceLocationUpdate'].get('ssid'),
            'rawUserId': event['deviceLocationUpdate'].get('rawUserId'),
            'ipv4': event['deviceLocationUpdate'].get('ipv4'),
            'ipv6': event['deviceLocationUpdate'].get('ipv6')
        }
    
    return filtered_event

def syslog_handler(event):
    try:
        # Filter out location information before sending
        filtered_event = filter_event(event)
        # Format event as JSON string
        event_str = json.dumps(filtered_event)
        # Send to syslog
        logger.info(event_str)
    except Exception as e:
        print(f"An error occurred while handling the event: {e}")
        print(json.dumps(event))

print("Starting system")    
stream()