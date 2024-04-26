from datetime import datetime, timedelta

# Function to generate URLs for monthly ranges
def generate_urls(start_date, end_date):
    base_url = "https://www.forexfactory.com/calendar?range="
    urls = []
    current_date = start_date
    while current_date < end_date:
        next_date = current_date + timedelta(days=1)
        url = f"{base_url}{current_date.strftime('%b%d.%Y')}-{next_date.strftime('%b%d.%Y')}"
        urls.append(url)
        current_date = next_date
    return urls


if __name__ == "__main__":
    # Starting date
    start_date = datetime(2021, 1, 1)

    # Ending date
    end_date = datetime.now()

    # Generate URLs
    urls = generate_urls(start_date, end_date)

    # Write generated URLs to a text file
    with open("generated_urls.txt", "w") as file:
        for url in urls:
            file.write(url + "\n")
