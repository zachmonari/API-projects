from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def home():
    return {"message":"Hello FastAPI Learner!"}

#GET Request with Path Parameter
@app.get("/student/{student_id}")
def get_student(student_id: int):
    return {"student_id": student_id}
#GET with Query Parameter
@app.get("/vibration/energy")
def compute_energy(amplitude: float, mass: float):
    return {"energy": 0.5 * mass * amplitude**2}
