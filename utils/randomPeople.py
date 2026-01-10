from PIL import Image, ImageDraw, ImageOps
from io import BytesIO
import requests
import os
from core.node import Identity, Person
import logging

logger = logging.getLogger(__name__)

def create_person(fname, lname, gender, picture = None):
    identity = Identity(fname, lname, gender, picture)
    return Person(identity)


def generate_random_batch(size: int, location):
    logger.info("\nGenerating People, Please Wait...")
    # one request, N results
    url = f"https://randomuser.me/api/?nat=us,gb,ca,au,nz&results={size}"
    resp = requests.get(url, timeout=3)
    resp.raise_for_status()

    results = resp.json().get("results", [])
    people = []

    for entry in results:
        fname = entry["name"]["first"].strip()
        lname = entry["name"]["last"].strip()
        gender = entry["gender"]
        picture_url = entry["picture"]["large"]

        # Catch unusual first name entries
        if " or " in fname:
            fname = fname.split(" or ")[0]
        elif "/" in fname:
            fname = fname.split("/")[0]

        people.append(create_person(fname, lname, gender))
        people[-1].data.picture = download_image(picture_url, people[-1], location)

    logger.info("Generation Complete!\n")
    return people


def download_image(url, person, location):
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
    except Exception as e:
        logger.warning(f"Image download failed: {e}")
        return None


    # Convert any format to real PNG in case API hates me
    img = Image.open(BytesIO(r.content)).convert("RGBA")

    # Resize + circular mask
    img = ImageOps.fit(img, (128, 128), centering=(0.5, 0.5))

    mask = Image.new("L", (128, 128), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 128, 128), fill=255)
    img.putalpha(mask)

    # Adjustable border rendering
    border_width = 12  # change to liking
    size = 128
    total = size + border_width * 2   # expanded canvas so border isn't cropped

    # Larger transparent canvas
    border = Image.new("RGBA", (total, total), (0, 0, 0, 0))
    draw = ImageDraw.Draw(border)

    # Draw border centered around image
    draw.ellipse(
        (border_width/2,
         border_width/2,
         total - border_width/2,
         total - border_width/2),
        outline=(0, 0, 0, 255),   # edit this for color/opacity
        width=border_width
    )

    # Paste circular portrait in the center
    border.paste(img, (border_width, border_width), img)

    # Replace img with final bordered version
    img = border

    # Save
    os.makedirs(f"assets/portraits/{location}", exist_ok=True)
    path = f"assets/portraits/{location}/{person.data.fname}_{person.data.lname}.png"
    
    img.save(path, format="PNG")

    return path


def build_set(size: int, location = "generated_set", existing = None):
    # Start with a fresh batch
    people = generate_random_batch(size, location)

    # Merge with existing if present
    if existing:
        people.extend(existing)

    # Deduplicate by full name
    seen = set()
    unique_people = []
    duplicates = 0

    for person in people:
        key = (person.data.fname, person.data.lname)

        if key not in seen:
            seen.add(key)
            unique_people.append(person)
        else:
            duplicates += 1

    # If duplicates exist, recursively generate replacements
    if duplicates > 0:
        return build_set(duplicates, location, unique_people)

    return unique_people

