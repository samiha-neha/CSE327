from .views import cart_summary

def cart_context(request):
    return {
        'cart_summary': cart_summary(request)
    }