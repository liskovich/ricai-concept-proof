# RicAI autonomous testing agent 

## Proof of concept

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
        # correct calculation
        # discounted_price = original_price - (original_price * discount_percentage / 100)
        
        # calculation with error (multiplying by 2 was not required)
        discounted_price = original_price - (2 * original_price * discount_percentage / 100)
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

| Test Case | Description | Expected Output |
| --- | --- | --- |
| Test Case 1 | Test with valid input: original_price = 100, discount_percentage = 10 | 90.0 |
| Test Case 2 | Test with valid input: original_price = 50, discount_percentage = 50 | 25.0 |
| Test Case 3 | Test with valid input: original_price = 200, discount_percentage = 25 | 150.0 |
| Test Case 4 | Test with invalid input: original_price = -100, discount_percentage = 10 | 'Invalid input: Original price must be greater than 0, and discount percentage must be between 0 and 100' |
| Test Case 5 | Test with invalid input: original_price = 100, discount_percentage = 150 | 'Invalid input: Original price must be greater than 0, and discount percentage must be between 0 and 100' |
| Test Case 6 | Test with invalid input: original_price = 0, discount_percentage = 50 | 'Invalid input: Original price must be greater than 0, and discount percentage must be between 0 and 100' |

The produced output of unit tests:

```python
import pytest

from your_module import calculate_discounted_price

def test_valid_input_case_1():
    original_price = 100
    discount_percentage = 10
    expected_output = 90.0

    assert calculate_discounted_price(original_price, discount_percentage) == expected_output

def test_valid_input_case_2():
    original_price = 50
    discount_percentage = 50
    expected_output = 25.0

    assert calculate_discounted_price(original_price, discount_percentage) == expected_output

def test_valid_input_case_3():
    original_price = 200
    discount_percentage = 25
    expected_output = 150.0

    assert calculate_discounted_price(original_price, discount_percentage) == expected_output

def test_invalid_input_case_4():
    original_price = -100
    discount_percentage = 10
    expected_output = 'Invalid input: Original price must be greater than 0, and discount percentage must be between 0 and 100'

    assert calculate_discounted_price(original_price, discount_percentage) == expected_output

def test_invalid_input_case_5():
    original_price = 100
    discount_percentage = 150
    expected_output = 'Invalid input: Original price must be greater than 0, and discount percentage must be between 0 and 100'

    assert calculate_discounted_price(original_price, discount_percentage) == expected_output

def test_invalid_input_case_6():
    original_price = 0
    discount_percentage = 50
    expected_output = 'Invalid input: Original price must be greater than 0, and discount percentage must be between 0 and 100'

    assert calculate_discounted_price(original_price, discount_percentage) == expected_output
```

When running these tests, we get the foollowing oucome:

|         filepath          |         function          | passed | failed | SUBTOTAL |
| ------------------------- | ------------------------- | -----: | -----: | -------: |
| tests\test_sample_code.py | test_valid_input_case_1   |      0 |      1 |        1 |
| tests\test_sample_code.py | test_valid_input_case_2   |      0 |      1 |        1 |
| tests\test_sample_code.py | test_valid_input_case_3   |      0 |      1 |        1 |
| tests\test_sample_code.py | test_invalid_input_case_4 |      1 |      0 |        1 |
| tests\test_sample_code.py | test_invalid_input_case_5 |      1 |      0 |        1 |
| tests\test_sample_code.py | test_invalid_input_case_6 |      1 |      0 |        1 |
| TOTAL                     |                           |      3 |      3 |        6 |

We see that some of the test cases failed (due to the error that is present in the function itself).
Next, we combine our faulty code, test descriptions, the result of running tests and the requirements in order to give feedback and propose fixes, then pass it to LLM. The result is the following:

```
Based on the code and the test results, here are some suggestions to improve the code:

1. Fix the calculation error in the `calculate_discounted_price` function. The line `discounted_price = original_price - (2 * original_price * discount_percentage / 100)` should be changed to `discounted_price = original_price - (original_price * discount_percentage / 100)`. The multiplication by 2 is not required.

2. Update the error message in the `else` block of the `calculate_discounted_price` function to provide more specific information about the invalid input. For example, instead of a generic message, you can specify that the original price must be greater than 0 and the discount percentage must be between 0 and 100.

3. Update the test cases to reflect the corrected calculation in the `calculate_discounted_price` function. The expected output values should be adjusted accordingly.

4. Review the failed test cases and ensure that the code is handling invalid input correctly. For example, the test case `test_invalid_input_case_4` should fail because the code is not correctly handling negative original prices. The code should return the same error message as specified in the test case.

5. Consider adding additional test cases to cover different scenarios, such as edge cases (e.g., original price = 0, discount percentage = 0) and boundary cases (e.g., original price = 1, discount percentage = 100).

By implementing these suggestions, you should be able to fix the bugs in the code and improve its functionality.
```

And here we can see that as the first point int the improvement list, is the suggestion to remove multiplication by 2, which is exactly what we would expect! There are also some other decent suggestions one might consider using.

## How to try it myself?

In order to try this out, create a `.env` file and add the following to it:
```env
OPEN_AI_KEY=<your_openai_api_key>
WEAVIATE_URL=<your_weaviate_cloud_url>
WEAVIATE_API_KEY=<your_weaviate_auth_token>
```

Then follow this step-by-step process:

1. Inside `main.py` uncomment the line 295 with `main()` call, run the `main.py` file.
2. If all goes well, you will receive a table with test case descriptions in markdown format and a `pytest` unit tests. Copy and paste the generated unit tests somewhere for later use. Comment out the line with `main()` call.
3. Create a new directory `tests` and paste the generate `pytest` unit tests in the file `tests/test_sample_code.py` (you might need to create it first).
4. Uncomment the line 301 with `run_tests()` call, run the `main.py` file.
5. Again, if all goes well, you will receive a table with test report in markdown format. Copy and paste it somewhere for later use. Comment out the line with `run_tests()` call.
6. Again, inside `main.py` uncomment the line 295 with `main()` call.
7. Find the function `generate_suggestions` and inside the two palceholders paste generated unit tests and test reports appropriately.
8. Uncomment the line 291 with `generate_suggestions(code_feature)` call, run the `main.py` file.
9. Finally, you will (hopefully) receive generated suggestions and recommendations in your cmd line!

Running the code may consume your OpenAI credits and take some time to execute!
