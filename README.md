# 🇮🇪 Adverts.ie Scraper - AI-Powered Irish Classifieds Extraction

[![Apify Actor](https://img.shields.io/badge/Apify-Actor-00D4FF?style=flat-square)](https://apify.com/fervent_bus/adverts-ie-scraper)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![AI Agent Compatible](https://img.shields.io/badge/AI-Claude%20%7C%20ChatGPT%20%7C%20MCP-blueviolet?style=flat-square)](https://apify.com)

Extract structured data from **Adverts.ie**, Ireland's trusted marketplace. Built for developers, AI agents (Claude, ChatGPT), and automation workflows via **Apify MCP integration**.

---

## ✨ Features

- 🤖 **AI Agent Ready** - Works seamlessly with Claude, ChatGPT, and other AI agents via Apify MCP
- 🔄 **Full Pagination** - Automatically scrapes multiple pages of listings
- 🌍 **County Filtering** - Target specific Irish counties or search nationwide
- 📊 **Multiple Export Formats** - JSON, CSV, Excel, HTML
- ⚡ **Fast & Reliable** - Optimized Cloudflare bypass with residential proxies
- 🛡️ **Anti-Bot Protection** - Handles Cloudflare and other protections with Camoufox
- 🔍 **Advanced Filtering** - Category, location, price range, and keyword search
- 💶 **Price Data** - Extract prices in EUR with automatic parsing

---

## 🚀 Quick Start

### Via Apify Console
1. Go to [Apify Console](https://console.apify.com/actors/fervent_bus~adverts-ie-scraper)
2. Configure input fields (category, county, price range, etc.)
3. Click **Run** and download results

### Via API (Python)
```python
from apify_client import ApifyClient

client = ApifyClient('YOUR_APIFY_TOKEN')

run = client.actor('fervent_bus/adverts-ie-scraper').call(run_input={
    'category': 'for-sale',
    'county': 'Dublin',
    'minPrice': 0,
    'maxPrice': 500,
    'searchQuery': 'iPhone',
    'maxResults': 50
})

# Fetch results
items = client.dataset(run['defaultDatasetId']).list_items().items
for item in items:
    print(f"{item['title']} - {item['price']}")
```

### Via API (JavaScript)
```javascript
const ApifyClient = require('apify-client');

const client = new ApifyClient({ token: 'YOUR_APIFY_TOKEN' });

const run = await client.actor('fervent_bus/adverts-ie-scraper').call({
    category: 'for-sale',
    county: 'Cork',
    searchQuery: 'bike',
    maxResults: 50
});

const { items } = await client.dataset(run.defaultDatasetId).listItems();
items.forEach(item => console.log(`${item.title} - ${item.price}`));
```

### Via cURL
```bash
curl -X POST https://api.apify.com/v2/acts/fervent_bus~adverts-ie-scraper/runs \
  -H "Authorization: Bearer YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"category": "for-sale", "county": "Galway", "maxResults": 50}'
```

---

## 📥 Input Configuration

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `category` | Select | Category to scrape (for-sale, motors, property, jobs, services) | ✅ |
| `subcategory` | String | Narrow down to specific subcategory (optional) | ❌ |
| `county` | Select | Irish county filter (leave empty for all Ireland) | ❌ |
| `minPrice` | Integer | Minimum price in EUR (default: 0) | ❌ |
| `maxPrice` | Integer | Maximum price in EUR (default: 999999) | ❌ |
| `searchQuery` | String | Keyword search within category (optional) | ❌ |
| `maxResults` | Integer | Maximum results to scrape (default: 3) | ❌ |
| `proxyConfiguration` | Object | Proxy settings (RESIDENTIAL group recommended) | ❌ |

---

## 📤 Output Structure

```json
[
  {
    "url": "https://www.adverts.ie/listing/123456",
    "title": "iPhone 13 Pro - 256GB",
    "price": "€450",
    "currency": "EUR",
    "location": "Dublin",
    "description": null,
    "image": "https://media.adverts.ie/images/listing.jpg",
    "category": "for-sale",
    "scrapedAt": "2026-10-06T14:30:00.000Z"
  }
]
```

### Field Descriptions
- **url** - Direct link to the listing on Adverts.ie
- **title** - Listing title/headline
- **price** - Listed price (string format with € symbol)
- **currency** - Price currency (EUR for Ireland)
- **location** - County or city in Ireland
- **description** - Full description (requires detail page visit - future enhancement)
- **image** - URL of the main listing image
- **category** - Category of the listing
- **scrapedAt** - ISO 8601 timestamp when data was collected

---

## 💡 Use Cases

### 🎯 Lead Generation
Extract business listings, contact sellers, and build prospect databases for sales outreach.

### 📊 Market Research
Monitor competitor listings, pricing trends, and inventory levels across Irish counties.

### 🏠 Real Estate Tracking
Track property listings, price changes, and availability in your target markets.

### 💰 Price Monitoring
Set up automated price tracking for products or services across categories.

### 🤖 AI Agent Workflows
Integrate with Claude Code, ChatGPT plugins, or custom AI agents via Apify MCP for automated data collection and analysis.

### 📈 Business Intelligence
Aggregate market data for strategic decision-making and trend analysis in the Irish market.

---

## ❓ FAQ

### Does it handle pagination?
Yes! The scraper automatically follows pagination links to collect all available results up to your `maxResults` limit.

### Can I filter by county?
Absolutely! Use the `county` parameter to target specific Irish counties like Dublin, Cork, Galway, etc., or leave empty for nationwide results.

### What export formats are supported?
JSON, CSV, Excel (XLSX), HTML, RSS, and XML. Download from Apify Console or fetch via API.

### Is it compatible with AI agents?
✅ **Yes!** This actor works with Claude Code, ChatGPT, and other AI agents through **Apify MCP integration**. Use it directly from your AI assistant.

### How often can I run it?
As often as you need! Runs are limited only by your Apify subscription plan.

### Does it bypass Cloudflare?
Yes, we use Camoufox browser automation with residential proxies and adaptive strategies to handle Cloudflare protection.

### What about proxy configuration?
We recommend using **RESIDENTIAL** proxy group for best results with Cloudflare-protected sites. Configure via `proxyConfiguration` input.

---

## 💰 Pricing

| Event Type | Price | Description |
|------------|-------|-------------|
| 💵 **Per Result** | $0.005 | Each listing/item scraped |
| 🚀 **Actor Start** | $0.05 | One-time fee per run |

**Example:** Scraping 100 results = $0.05 (start) + $0.50 (100 × $0.005) = **$0.55 total**

[View detailed pricing](https://apify.com/fervent_bus/adverts-ie-scraper/pricing)

---

## 🔗 Links

- 🏠 [Actor Page](https://apify.com/fervent_bus/adverts-ie-scraper)
- 📚 [Apify Documentation](https://docs.apify.com)
- 💬 [Support](https://console.apify.com/actors/fervent_bus~adverts-ie-scraper/issues)
- 🐙 [GitHub Repository](https://github.com/roshtarg-cpu/adverts-ie-scraper)

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

**Built with ❤️ for developers and AI agents. Compatible with Claude, ChatGPT & AI automation via Apify MCP.**
