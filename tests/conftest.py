import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--test-cases",
        action="store",
        default="",  # "weather" # default is don't run any
        help="Comma-separated list of test case names to run, e.g., 'weather'",
    )


@pytest.fixture
def test_use_cases(request):
    def check_all_keywords(response, keywords):
        return all(keyword.lower() in response.lower() for keyword in keywords)

    def check_any_keyword(response, keywords):
        return any(keyword.lower() in response.lower() for keyword in keywords)

    all_cases = {
        "weather": {
            "prompt": "what is 1+1 and how is the weather in bengaluru and mumbai?",
            "user_id": "test_user_1",
            "expected_keywords": ["2", "bengaluru", "mumbai"],
            "check_function": check_all_keywords,
        },
    }
    selected_tests = request.config.getoption("--test-cases").split(",")
    return [all_cases[test] for test in selected_tests if test in all_cases]
