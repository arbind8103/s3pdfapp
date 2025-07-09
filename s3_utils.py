import boto3
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

BUCKET_NAME = "bills-pos"
PREFIX = "POS/"
REGION = "ap-south-1"

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=REGION
)

def search_files(query="", start_date="", end_date="", file_type="", sort_by="newest"):
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=PREFIX)
    files = []

    for obj in response.get("Contents", []):
        key = obj["Key"]
        if key.endswith("/"):
            continue
        name = key.replace(PREFIX, "")
        last_modified = obj["LastModified"]

        if query.lower() not in name.lower():
            continue

        if file_type and not name.lower().endswith(file_type.lower()):
            continue

        if start_date:
            sd = datetime.strptime(start_date, "%Y-%m-%d")
            if last_modified.date() < sd.date():
                continue

        if end_date:
            ed = datetime.strptime(end_date, "%Y-%m-%d")
            if last_modified.date() > ed.date():
                continue

        files.append({
            "name": name,
            "url": s3.generate_presigned_url("get_object", Params={"Bucket": BUCKET_NAME, "Key": key}, ExpiresIn=3600),
            "last_modified": last_modified.strftime("%Y-%m-%d %H:%M")
        })

    if sort_by == "az":
        files.sort(key=lambda x: x["name"].lower())
    elif sort_by == "za":
        files.sort(key=lambda x: x["name"].lower(), reverse=True)
    elif sort_by == "oldest":
        files.sort(key=lambda x: x["last_modified"])
    else:
        files.sort(key=lambda x: x["last_modified"], reverse=True)

    return files
