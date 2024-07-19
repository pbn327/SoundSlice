from fastapi import FastAPI

app = FastAPI()

# Define a root `/` endpoint
@app.get('/')
def index():
    return {'ok': True}


@app.get('/separate')
def predict(day_of_week, time):
    # Compute `wait_prediction` from `day_of_week` and `time`
    wait_prediction = int(day_of_week) * int(time)

    return {'wait': wait_prediction}
