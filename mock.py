import time
import random
from typing import Dict

# This is the function given in the pdf
def mock_model_predict(input: str) -> Dict[str, str]:
    time.sleep(random.randint(10, 17)) # Simulate processing delay
    result = str(random.randint(1000, 20000))
    output = {"input": input, "result": result}
    return output