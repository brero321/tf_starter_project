import json
from unittest.mock import MagicMock
from example import lambda_handler, calculate_volume

def test_lambda_handler_calculates_volume():
    """Test that lambda_handler calculates and returns volume"""
    # Arrange
    event = {'length': 2, 'width': 3, 'height': 4}
    context = MagicMock()
    context.log_group_name = '/aws/lambda/test-function'
    
    # Act
    response = lambda_handler(event, context)
    
    # Assert
    response_data = json.loads(response)
    assert response_data['volume'] == 24  # 2 * 3 * 4

def test_calculate_volume_with_invalid_input():
    """Test that calculate_volume rejects invalid input"""
    try:
        calculate_volume(-5, 3, 4)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "positive" in str(e)