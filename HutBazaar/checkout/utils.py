from .models import Discount


def apply_discount(cart, coupon_code):
    try:
        discount = Discount.objects.get(code=coupon_code, active=True)
        if discount.discount_type == "percentage":
            discount_amount = cart.total * (discount.amount / 100)
        else:
            discount_amount = discount.amount

        cart.total -= discount_amount
        cart.save()
        return True, discount_amount
    except Discount.DoesNotExist:
        return False, 0
