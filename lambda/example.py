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
    
    volume = calculate_volume(length, width, height)
    print(f"The volume is {volume}")
        
    logger.info(f"CloudWatch logs group: {context.log_group_name}")
    
    # return the calculated area as a JSON string
    data = {"volume": volume}
    return json.dumps(data)
    
def calculate_volume(length, width, height):
    """Calculate volume
    
    Args:
        length, width, height: positive numbers
    
    Raises:
        TypeError: if inputs are not numbers
        ValueError: if any input is <= 0 or NaN
    """
    # Quick sanity checks (fail loudly if someone misuses)
    for dim, name in [(length, 'length'), (width, 'width'), (height, 'height')]:
        if not isinstance(dim, (int, float)):
            raise TypeError(f"{name} must be a number")
        if dim != dim:  # NaN
            raise ValueError(f"{name} is NaN")
        if dim <= 0:
            raise ValueError(f"{name} must be positive")
    
    return length * width * height