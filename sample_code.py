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
