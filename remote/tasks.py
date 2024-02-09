import dramatiq
from .models import CompletedUK
@dramatiq.actor
def test_dramatiq(a):
    print(123123)