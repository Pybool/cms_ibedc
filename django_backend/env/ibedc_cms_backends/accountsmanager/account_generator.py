import time
import random
from datetime import date

def generate_account_no():
    def get_entropy():
        entropy = random.randint(200,299)
        return str(entropy)
    epoch = time.time()
    user_id = get_entropy()
    unique_id = "%s%d" % (user_id, epoch)
    return unique_id

