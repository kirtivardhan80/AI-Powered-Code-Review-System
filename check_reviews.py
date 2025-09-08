import asyncio
from db import reviews_collection  # Import your MongoDB collection

async def main():
    # Fetch up to 100 reviews
    reviews = await reviews_collection.find().to_list(100)
    
    if not reviews:
        print("No reviews found in the database.")
        return

    for idx, r in enumerate(reviews, 1):
        print(f"--- Review #{idx} ---")
        print("ID:", r.get("_id"))
        print("Language Detected:", r.get("language_detected"))
        print("Issues:")
        for issue in r.get("issues", []):
            print("  -", issue)
        print("Suggestions:")
        for suggestion in r.get("suggestions", []):
            print("  -", suggestion)
        print("Improved Code:\n", r.get("improved_code"))
        print("Details:", r.get("details"))
        print("\n" + "="*50 + "\n")

# Run the async function
asyncio.run(main())
