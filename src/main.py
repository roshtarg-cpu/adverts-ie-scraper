"""Adverts.ie scraper - Irish classifieds marketplace."""
import asyncio
from datetime import datetime, timezone
from typing import Any, Dict
from urllib.parse import urlencode

from apify import Actor
from camoufox.async_api import AsyncCamoufox
from bs4 import BeautifulSoup


async def main() -> None:
    """Main scraper entry point."""
    async with Actor:
        # Get input (NO await - synchronous in SDK 4.x)
        actor_input = Actor.get_env()
        input_data = await Actor.get_input() or {}
        
        # Extract parameters
        category = input_data.get("category", "for-sale")
        subcategory = input_data.get("subcategory", "")
        county = input_data.get("county", "")
        min_price = input_data.get("minPrice", 0)
        max_price = input_data.get("maxPrice", 999999)
        search_query = input_data.get("searchQuery", "")
        max_results = input_data.get("maxResults", 3)
        proxy_config = input_data.get("proxyConfiguration", {
            "useApifyProxy": True,
            "apifyProxyGroups": ["RESIDENTIAL"]
        })
        
        Actor.log.info(f"Starting Adverts.ie scraper")  # NO await
        Actor.log.info(f"Category: {category}, County: {county or 'All'}")
        Actor.log.info(f"Max results: {max_results}")
        
        # Build search URL
        base_url = "https://www.adverts.ie"
        
        # Construct path
        if subcategory:
            url_path = f"/{category}/{subcategory}"
        else:
            url_path = f"/{category}"
        
        # Add county filter
        if county:
            url_path += f"/county-{county}"
        
        # Add search query
        if search_query:
            url_path = f"/results/{search_query}"
        
        search_url = f"{base_url}{url_path}"
        
        Actor.log.info(f"Search URL: {search_url}")
        
        # Get proxy URL
        proxy_url = None
        if proxy_config.get("useApifyProxy"):
            groups = proxy_config.get("apifyProxyGroups", ["RESIDENTIAL"])
            proxy_url = Actor.create_proxy_url(groups=groups)
        
        # Launch Camoufox browser
        Actor.log.info("Launching browser with Camoufox...")
        
        async with AsyncCamoufox(
            headless=True,
            proxy=proxy_url
        ) as browser:
            page = await browser.new_page()
            
            # Navigate to search page
            Actor.log.info(f"Navigating to {search_url}")
            await page.goto(search_url, wait_until="domcontentloaded", timeout=60000)
            
            # Wait for listings to load
            await asyncio.sleep(3)
            
            # Get page content
            content = await page.content()
            soup = BeautifulSoup(content, "html.parser")
            
            # Find listing containers - additive multi-strategy approach
            containers = set()
            
            # Strategy 1: data attributes
            for elem in soup.find_all(attrs={"data-listing-id": True}):
                containers.add(elem)
            
            for elem in soup.find_all(attrs={"data-testid": lambda x: x and ("listing" in x or "card" in x)}):
                containers.add(elem)
            
            # Strategy 2: article tags
            for elem in soup.find_all("article"):
                if elem.find("a"):
                    containers.add(elem)
            
            # Strategy 3: common class patterns
            if not containers:
                for elem in soup.find_all("div", class_=lambda x: x and any(
                    term in x.lower() for term in ["listing", "item", "card", "advert", "result"]
                )):
                    containers.add(elem)
            
            # Strategy 4: li elements
            if not containers:
                for elem in soup.find_all("li", class_=lambda x: x and any(
                    term in x.lower() for term in ["listing", "item", "result"]
                )):
                    containers.add(elem)
            
            Actor.log.info(f"Found {len(containers)} listing containers")
            
            if not containers:
                Actor.log.error("No listings found - check selectors or site structure changed")
                await Actor.set_value("SAVED-TASK", {
                    "actorId": actor_input.get("actor_id"),
                    "actorRunId": actor_input.get("actor_run_id"),
                    "defaultDatasetId": actor_input.get("default_dataset_id"),
                    "startedAt": datetime.now(timezone.utc).isoformat(),
                    "input": input_data,
                    "stats": {"items": 0, "errors": 1}
                })
                return
            
            # Extract data from containers
            results_count = 0
            
            for container in list(containers)[:max_results]:
                try:
                    # Extract title
                    title_elem = container.find(["h1", "h2", "h3", "h4", "a"])
                    title = title_elem.get_text().strip() if title_elem else None
                    
                    # Extract URL
                    link_elem = container.find("a", href=True)
                    url = None
                    if link_elem:
                        href = link_elem["href"]
                        url = href if href.startswith("http") else f"{base_url}{href}"
                    
                    # Extract price
                    price_elem = container.find(string=lambda x: x and "€" in x)
                    price = price_elem.strip() if price_elem else None
                    
                    # Extract image
                    img_elem = container.find("img", src=True)
                    image = img_elem["src"] if img_elem else None
                    if image and not image.startswith("http"):
                        image = f"{base_url}{image}"
                    
                    # Extract location (look for county names)
                    location = None
                    location_elem = container.find(string=lambda x: x and any(
                        county_name in x for county_name in [
                            "Dublin", "Cork", "Galway", "Limerick", "Waterford",
                            "Kerry", "Clare", "Donegal", "Mayo", "Meath"
                        ]
                    ))
                    if location_elem:
                        location = location_elem.strip()
                    
                    # Build result object
                    result = {
                        "url": url,
                        "title": title,
                        "price": price,
                        "currency": "EUR" if price else None,
                        "location": location,
                        "description": None,  # Would need detail page visit
                        "image": image,
                        "category": category,
                        "scrapedAt": datetime.now(timezone.utc).isoformat()
                    }
                    
                    # Push to dataset immediately
                    await Actor.push_data(result)
                    results_count += 1
                    
                    if results_count % 10 == 0:
                        Actor.log.info(f"Scraped {results_count} items so far")
                    
                    if results_count >= max_results:
                        break
                    
                except Exception as e:
                    Actor.log.warning(f"Failed to extract listing: {e}")
                    continue
            
            Actor.log.info(f"✓ Scraping complete: {results_count} items")
            
            # Save task metadata
            await Actor.set_value("SAVED-TASK", {
                "actorId": actor_input.get("actor_id"),
                "actorRunId": actor_input.get("actor_run_id"),
                "defaultDatasetId": actor_input.get("default_dataset_id"),
                "startedAt": datetime.now(timezone.utc).isoformat(),
                "input": input_data,
                "stats": {"items": results_count, "errors": 0}
            })
