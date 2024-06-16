from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from models import Base, engine, SessionLocal, User

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def get_form():
    return """
    <html>
        <head>
            <title>User Details Form</title>
        </head>
        <body>
            <h2>User Details Form</h2>
            <p>Before we start, what is your name?</p>
            <form method="post" action="/submit">
                <label for="first_name">First Name:</label><br>
                <input type="text" id="first_name" name="first_name"><br>
                <label for="last_name">Last Name:</label><br>
                <input type="text" id="last_name" name="last_name"><br>
                <br>
                <label for="email">What's your email address?</label><br>
                <input type="email" id="email" name="email"><br>
                <br>
                <label for="country">Which country you are from?</label><br>
                <input type="text" id="country" name="country"><br>
                <br>
                <label for="phone_number">What is your phone number?</label><br>
                <input type="text" id="phone_number" name="phone_number"><br>
                <br>
                <label for="languages">What languages and frameworks are you familiar with?</label><br>
                <input type="text" id="languages" name="languages"><br>
                <br>
                <label for="experience">How would you describe your current level of coding experience?</label><br>
                <input type="number" id="experience" name="experience"><br>
                <br>
                <label for="annual_salary">What is your current annual compensation?</label><br>
                <p>Disclaimer: The information provided regarding salary will be kept confidential and will not be used 
                as a determining factor for acceptance into the bootcamp. It will be used exclusively 
                for career advancement guidance.</p>
                <input type="number" step="0.01" id="annual_salary" name="annual_salary"><br><br>
                <button type="submit" name="action" value="accept">Accept</button>
                <button type="submit" name="action" value="reject">Reject</button>
            </form>
        </body>
    </html>
    """

@app.post("/submit")
async def handle_form(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    country: str = Form(...),
    phone_number: str = Form(...),
    languages: str = Form(...),
    experience: int = Form(...),
    annual_salary: float = Form(...),
    action: str = Form(...),
    db: Session = Depends(get_db)
):
    if action == "accept":
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            country=country,
            phone_number=phone_number,
            languages=languages,
            experience=experience,
            annual_salary=annual_salary,
        )
        db.add(user)
        db.commit()
        return HTMLResponse("User accepted and data saved.")
    else:
        return HTMLResponse("User rejected.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)