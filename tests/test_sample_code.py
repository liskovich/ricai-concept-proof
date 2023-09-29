import pytest

from sample_code import calculate_discounted_price

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
