
from typing import Annotated

from langchain.tools import tool
import serpapi
from firecrawl import Firecrawl
from dotenv import load_dotenv
import os

load_dotenv()


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or value == "":
        raise ValueError(f"Missing required environment variable: {name}")
    return value


@tool('light_search', description= "search the internet with search api")

def light_search(search_term: str):

    client = serpapi.Client(api_key=_require_env('SERP_API_KEY'))

    results = client.search({

        "engine" : "google",
        "q": search_term,
        "location" :"Austin, Texas, United States", # TODO  : Replace with the users actual location
        "google_domain" : "google.com",
        "hl":"en",
        "gl":"us"


    })

    if 'organic_results' not in results:

        return 'This search term did not turn up good results'

    else:

        return results['organic_results'][:5] #TODO: hmmm, jev could probably 'sift' these results and surface the best ones



@tool('url_context', description="Get full page context from a *specific* URL, use crawl if you're not sure of the specific URL")

def url_context(
    url: Annotated[str, "URL to visit for context"], 
    extraction_prompt: Annotated[str | None, "Prompt to hand off to structured data extraction, ONLY REQUIRED if performing structured extraction ie; Job site, statistics"] = "", 
    extraction_schema: Annotated[dict  | None, " Valid JSON schema for extracted data, ideal for export prep"] = None):

    firecrawl_client = (
        Firecrawl(api_key=_require_env('FIRE_API_KEY'))
        if os.getenv('FIRE_API_KEY')
        else Firecrawl()
    )

    context = ''

    try:
        if not extraction_prompt:
            context = firecrawl_client.scrape(url, formats=['markdown', 'html'])
        else:
            extract_kwargs = {
                'prompt': extraction_prompt,
                'schema': extraction_schema,
            }

            scrape_url = getattr(firecrawl_client, 'v1', None)
            if scrape_url is not None and hasattr(scrape_url, 'scrape_url'):
                context = scrape_url.scrape_url(
                    url,
                    formats=['extract'],
                    extract=extract_kwargs,
                )
            else:
                context = firecrawl_client.scrape_url(
                    url,
                    formats=['extract'],
                    extract=extract_kwargs,
                )

    except Exception as e:
        return f"Failed to fetch page context: {str(e)}"

    if not context:
        return 'This page did not return usable context, try to crawl it'

    return context



@tool('crawl_website', description="Crawl a website starting from its origin url")
def crawl_website(
    starting_url: Annotated[str,"URL to start scraping from"], 
    limit: Annotated[int | None, "Depth to travel from origin url"] = 5, 
    poll_interval :Annotated[int ,"Frequency of polling crawl job, measured in seconds, longer polls maybe required for large / complex websites"] = 1, 
    timeout: Annotated[int | None, "Timeout to allot before crawl job is terminated, measured in seconds,  longer timeouts may be required for large sites or sites with aggressive rate-limiting "] = 120 ):

    firecrawl_client = (
        Firecrawl(api_key=_require_env('FIRE_API_KEY'))
        if os.getenv('FIRE_API_KEY')
        else Firecrawl()
    )

    # poll_interval = poll_interval if poll_interval else 1
    timeout = timeout if timeout and timeout < 500 else 120
    limit = limit if limit and limit < 10 else 5



    job = firecrawl_client.crawl(url=starting_url, limit=limit, poll_interval= poll_interval  , timeout=timeout)

    return (job.status, job.data)









