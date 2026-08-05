import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    
    # Get the length and width parameters from the event object. The 
    # runtime converts the event object to a Python dictionary
    length = event['length']
    width = event['width']
    height = event['height']
    
    height = calculate_area(length, width, height)
    print(f"The volume is {volume}")
        
    logger.info(f"CloudWatch logs group: {context.log_group_name}")
    
    # return the calculated area as a JSON string
    data = {"volume": volume}
    return json.dumps(data)
    
def calculate_volume(length, width, height):
    return length*width*height