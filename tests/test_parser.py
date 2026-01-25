from src.parser import get_status_code_from_response

def test_parser_response(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    result = get_status_code_from_response(mock_response)

    assert result == 200