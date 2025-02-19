import pytest

from smolagents.default_tools import DuckDuckGoSearchTool, GoogleSearchTool, SpeechToTextTool, VisitWebpageTool
from smolagents.tool_validation import validate_tool_attributes
from smolagents.tools import Tool


@pytest.mark.parametrize("tool_class", [DuckDuckGoSearchTool, GoogleSearchTool, SpeechToTextTool, VisitWebpageTool])
def test_validate_tool_attributes_with_default_tools(tool_class):
    assert validate_tool_attributes(tool_class) is None, f"failed for {tool_class.name} tool"


class ValidTool(Tool):
    name = "valid_tool"
    description = "A valid tool"
    inputs = {"input": {"type": "string", "description": "input"}}
    output_type = "string"
    simple_attr = "string"
    dict_attr = {"key": "value"}

    def __init__(self, optional_param="default"):
        super().__init__()
        self.param = optional_param

    def forward(self, input: str) -> str:
        return input.upper()


def test_validate_tool_attributes_valid():
    assert validate_tool_attributes(ValidTool) is None


class InvalidToolRequiredParams(Tool):
    name = "invalid_tool"
    description = "Tool with required params"
    inputs = {"input": {"type": "string", "description": "input"}}
    output_type = "string"

    def __init__(self, required_param):  # No default value
        super().__init__()
        self.param = required_param

    def forward(self, input: str) -> str:
        return input


class InvalidToolComplexAttrs(Tool):
    name = "invalid_tool"
    description = "Tool with complex class attributes"
    inputs = {"input": {"type": "string", "description": "input"}}
    output_type = "string"
    complex_attr = [x for x in range(3)]  # Complex class attribute

    def __init__(self):
        super().__init__()

    def forward(self, input: str) -> str:
        return input


undefined_variable = "undefined_variable"


class InvalidToolUndefinedNames(Tool):
    name = "invalid_tool"
    description = "Tool with undefined names"
    inputs = {"input": {"type": "string", "description": "input"}}
    output_type = "string"

    def forward(self, input: str) -> str:
        return undefined_variable  # Undefined name


class InvalidToolNonLiteralDefaultParam(Tool):
    name = "invalid_tool"
    description = "Tool with non-literal default parameter value"
    inputs = {"input": {"type": "string", "description": "input"}}
    output_type = "string"

    def __init__(self, default_param=undefined_variable):  # undefined_variable as default is non-literal
        super().__init__()
        self.default_param = default_param

    def forward(self, input: str) -> str:
        return input


@pytest.mark.parametrize(
    "tool_class, expected_error",
    [
        (InvalidToolRequiredParams, "required arguments in __init__"),
        (InvalidToolComplexAttrs, "Complex attributes should be defined in __init"),
        (InvalidToolUndefinedNames, "Name 'undefined_variable' is undefined"),
        (InvalidToolNonLiteralDefaultParam, "Tool validation failed"),  # TODO: Improve error message
    ],
)
def test_validate_tool_attributes_exceptions(tool_class, expected_error):
    with pytest.raises(ValueError, match=expected_error):
        validate_tool_attributes(tool_class)
