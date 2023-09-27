# RicAI autonomous testing agent 

## Proof of concept

Build using Weaviate and Llama index

This repository is a super-simple presentation or idea of how the autonomous testing agent works.

Here is a hackathon solution: [github repo](https://github.com/liskovich/RicAI_Autonomous_Agents_Hackathon)

It takes code and software requirements specification as input, and produces tests as output which can then be run on a CI/CD pipeline for example. For the sake of simplicity, only the test generation part is demonstrated.

## Example

The given code as input:
```python
def calculate_square_area(side_length):
    if side_length > 0:
        area = side_length * side_length
        return area
    else:
        return 'Invalid input: Side length must be greater than 0'

def calculate_discounted_price(original_price, discount_percentage):
    if original_price > 0 and 0 <= discount_percentage <= 100:
        discounted_price = original_price - (original_price * discount_percentage / 100)
        return discounted_price
    else:
        return 'Invalid input: Original price must be greater than 0, and discount percentage must be between 0 and 100'
```

The given SRS (software requirements specification) as input:
```
## Introduction
The software described in this document consists of two Python functions, `calculate_square_area` and `calculate_discounted_price`, which perform specific calculations and include conditional statements to validate input parameters. These functions are intended for general-purpose use and can be integrated into various applications.

## Purpose
The purpose of this software is to provide users with the capability to calculate the area of a square and the discounted price of an item based on specified input parameters.

## Functionality

### `calculate_square_area` Function
#### Description
The `calculate_square_area` function calculates the area of a square based on the length of its side.

#### Input Parameters
- `side_length` (float or int): The length of the side of the square.

#### Output
- If `side_length` is greater than 0, the function returns the calculated area (float).
- If `side_length` is not greater than 0, the function returns an error message as a string: "Invalid input: Side length must be greater than 0."

### `calculate_discounted_price` Function
#### Description
The `calculate_discounted_price` function calculates the discounted price of an item based on the original price and a discount percentage.

#### Input Parameters
- `original_price` (float or int): The original price of the item.
- `discount_percentage` (float or int): The discount percentage to be applied to the original price.

#### Output
- If both `original_price` and `discount_percentage` are valid (original_price > 0 and 0 <= discount_percentage <= 100), the function returns the calculated discounted price (float).
- If either `original_price` is not greater than 0 or `discount_percentage` is not within the valid range, the function returns an error message as a string: "Invalid input: Original price must be greater than 0, and discount percentage must be between 0 and 100."

## Non-Functional Requirements
- **Usability**: The functions should be easy to use and understand.
- **Robustness**: The functions should handle invalid input gracefully and provide clear error messages.
- **Performance**: The functions should execute efficiently for typical input values.

## Dependencies
The software has no external dependencies and can be used in any Python environment that supports the required language features.
```

The produced output of test case descriptions:

| Test Case | Description |
| --- | --- |
| Test Case 1 | Verify that the function returns the correct discounted price when the original price and discount percentage are valid |
| Test Case 2 | Verify that the function returns an error message when the original price is less than or equal to 0 |
| Test Case 3 | Verify that the function returns an error message when the discount percentage is less than 0 |
| Test Case 4 | Verify that the function returns an error message when the discount percentage is greater than 100 |
| Test Case 5 | Verify that the function returns an error message when both the original price and discount percentage are invalid |
| Test Case 6 | Verify that the function returns an error message when the original price is valid but the discount percentage is invalid |
| Test Case 7 | Verify that the function returns an error message when the original price is invalid but the discount percentage is valid |

The produced output of unit tests:

```python
import pytest
from my_module import calculate_discounted_price

# Test Case 1
def test_calculate_discounted_price_valid_input():
    original_price = 100
    discount_percentage = 20
    expected_discounted_price = 80

    assert calculate_discounted_price(original_price, discount_percentage) == expected_discounted_price

# Test Case 2
def test_calculate_discounted_price_invalid_original_price():
    original_price = 0
    discount_percentage = 20
    expected_error_message = "Invalid original price"

    assert calculate_discounted_price(original_price, discount_percentage) == expected_error_message

# Test Case 3
def test_calculate_discounted_price_invalid_discount_percentage():
    original_price = 100
    discount_percentage = -10
    expected_error_message = "Invalid discount percentage"

    assert calculate_discounted_price(original_price, discount_percentage) == expected_error_message

# Test Case 4
def test_calculate_discounted_price_invalid_discount_percentage():
    original_price = 100
    discount_percentage = 110
    expected_error_message = "Invalid discount percentage"

    assert calculate_discounted_price(original_price, discount_percentage) == expected_error_message

# Test Case 5
def test_calculate_discounted_price_invalid_input():
    original_price = 0
    discount_percentage = -10
    expected_error_message = "Invalid original price and discount percentage"

    assert calculate_discounted_price(original_price, discount_percentage) == expected_error_message

# Test Case 6
def test_calculate_discounted_price_invalid_discount_percentage():
    original_price = 100
    discount_percentage = -10
    expected_error_message = "Invalid discount percentage"

    assert calculate_discounted_price(original_price, discount_percentage) == expected_error_message

# Test Case 7
def test_calculate_discounted_price_invalid_original_price():
    original_price = 0
    discount_percentage = 20
    expected_error_message = "Invalid original price"

    assert calculate_discounted_price(original_price, discount_percentage) == expected_error_message
```

## How to try it myself?

In order to try this out, create a `.env` file and add the following to it:
```env
OPEN_AI_KEY=<your_openai_api_key>
WEAVIATE_URL=<your_weaviate_cloud_url>
WEAVIATE_API_KEY=<your_weaviate_auth_token>
```

And run the `main.py` file

Running the code may consume your OpenAI credits and take some time to execute!
