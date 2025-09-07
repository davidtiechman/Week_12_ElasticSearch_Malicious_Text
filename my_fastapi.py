import uvicorn
from connect_elastics.get_elastics import GetElastic
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from connect_elastics.main import run_pipeline
import threading
import logging

app = FastAPI()
processing_done = False  # דגל גלובלי
logging.basicConfig(level=logging.DEBUG)


def background_pipeline():
    global processing_done
    logging.info("Starting pipeline in background...")
    run_pipeline()
    processing_done = True
    logging.info("Pipeline finished!")


@app.get("/antisemitic_with_weapon")
def antisemitic_with_weapon():
    if not processing_done:
        return JSONResponse(content={"message": "Data has not been fully processed yet."}, status_code=202)

    get_elastic = GetElastic()
    results = get_elastic.read_all("match_all")
    docs = list(results)

    filtered = [
        doc for doc in docs
        if doc.get("_source", {}).get("Antisemitic", 0) == 1
        and doc.get("_source", {}).get("weapons_detected")
    ]
    return JSONResponse(content=filtered, status_code=200)


@app.get("/multiple_weapons")
def multiple_weapons():
    if not processing_done:
        return JSONResponse(content={"message": "Data has not been fully processed yet."}, status_code=202)

    get_elastic = GetElastic()
    results = get_elastic.read_all("match_all")
    docs = list(results)

    filtered = [
        doc for doc in docs
        if len(doc.get("_source", {}).get("weapons_detected", [])) >= 2
    ]
    return JSONResponse(content=filtered, status_code=200)


if __name__ == "__main__":
    logging.info("Starting pipeline in background...")
    # מריצים את הפייפליין ברקע (thread)
    t = threading.Thread(target=background_pipeline)
    t.start()

    # השרת זמין מיד
    uvicorn.run(app, host="0.0.0.0", port=5000)
