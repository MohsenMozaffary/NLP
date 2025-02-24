from inspect import Parameter
from pydantic import create_model
import inspect
from duckduckgo_search import DDGS


def function_to_json(f):
    keywords = {}

        
    for name, metadata in inspect.signature(f).parameters.items():
        annotation = metadata.annotation
        if metadata.default == Parameter.empty:
            default_value = ...
        else:
            default_value = metadata.default
            
        keywords[name] = (annotation, default_value)
    
    parameters = create_model(f'The arguments for `{f.__name__}`', **keywords).model_json_schema()
    description = f.__doc__
    name = f.__name__
    json_model = dict(name = name, description = description ,parameters = parameters)
    return json_model

def text_search(keywords: str,
        region: str = "wt-wt",
        safesearch: str = "moderate",
        timelimit: str | None = None,
        backend: str = "auto",
        max_results: int | None = None,
        ) -> list[dict[str, str]]:
    
    """
    Searching web for keyword using duckduckgo.
    Args:
        keywords: keywords for query.
        region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
        safesearch: on, moderate, off. Defaults to "moderate".
        timelimit: d, w, m, y. Defaults to None.
        backend: auto, html, lite. Defaults to auto.
            auto - try all backends in random order,
            html - collect data from https://html.duckduckgo.com,
            lite - collect data from https://lite.duckduckgo.com.
        max_results: max number of results. If None, returns results only from the first response. Defaults to None.

    Returns:
        List of dictionaries with search results.
    """
    
    
    results = DDGS().text(keywords, region = region, safesearch = safesearch, timelimit = timelimit, max_results = max_results)
    
    return results

def pdf_search(
    keywords: str,
    region: str = "wt-wt",
    safesearch: str = "moderate",
    timelimit: str | None = None,
    backend: str = "auto",
    max_results: int | None = None,
) -> list[dict[str, str]]:
    """
    Searching web for pdfs with the keywords using duckduckgo.
    Args:
        keywords: pdf keywords for query.
        region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
        safesearch: on, moderate, off. Defaults to "moderate".
        timelimit: d, w, m, y. Defaults to None.
        backend: auto, html, lite. Defaults to auto.
            auto - try all backends in random order,
            html - collect data from https://html.duckduckgo.com,
            lite - collect data from https://lite.duckduckgo.com.
        max_results: max number of results. If None, returns results only from the first response. Defaults to None.

    Returns:
        List of dictionaries with pdf search results.
    """
    results = DDGS().text(
        "{}:pdf".format(keywords),
        region=region,
        safesearch=safesearch,
        timelimit=timelimit,
        max_results=max_results,
    )

    return results

def image_search( keywords: str,
    region: str = "wt-wt",
    safesearch: str = "moderate",
    timelimit: str | None = None,
    size: str | None = None,
    color: str | None = None,
    type_image: str | None = None,
    layout: str | None = None,
    license_image: str | None = None,
    max_results: int | None = None,
    ) -> list[dict[str, str]]:
    
    
    """
    Searching web for images.

    Args:
        keywords: keywords for query.
        region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
        safesearch: on, moderate, off. Defaults to "moderate".
        timelimit: Day, Week, Month, Year.
        size: Small, Medium, Large, Wallpaper.
        color: color, Monochrome, Red, Orange, Yellow, Green, Blue,
            Purple, Pink, Brown, Black, Gray, Teal, White.
        type_image: photo, clipart, gif, transparent, line.
        layout: Square, Tall, Wide.
        max_results: max number of results. If None, returns results only from the first response.

    Returns:
        List of dictionaries with images search results.
    """
    
    results = DDGS().images(
    keywords=keywords,
    region=region,
    safesearch=safesearch,
    size=size,
    color=color,
    type_image=type_image,
    layout=layout,
    license_image=license_image,
    max_results=max_results,
    )
    
    return results

def video_search(keywords: str,
    region: str = "wt-wt",
    safesearch: str = "moderate",
    timelimit: str | None = None,
    resolution: str | None = None,
    duration: str | None = None,
    license_videos: str | None = None,
    max_results: int | None = None,
    ) -> list[dict[str, str]]:
    
    """Searching web for videos related to the keywords using duckduckgo.

    Args:
        keywords: keywords for query.
        region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
        safesearch: on, moderate, off. Defaults to "moderate".
        timelimit: d, w, m. Defaults to None.
        resolution: high, standart. Defaults to None.
        duration: short, medium, long. Defaults to None.
        license_videos: creativeCommon, youtube. Defaults to None.
        max_results: max number of results. If None, returns results only from the first response. Defaults to None.

    Returns:
        List of dictionaries with videos search results.
    """
    
    results = DDGS().videos(
    keywords=keywords,
    region=region,
    safesearch=safesearch,
    timelimit=timelimit,
    resolution=resolution,
    duration=duration,
    max_results=max_results,
    )
    
    return results

def news_search(keywords: str,
    region: str = "wt-wt",
    safesearch: str = "moderate",
    timelimit: str | None = None,
    max_results: int | None = None,
    ) -> list[dict[str, str]]:
    
    """Searching web for news related to the keywords using duckduckgo

    Args:
        keywords: keywords for query.
        region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
        safesearch: on, moderate, off. Defaults to "moderate".
        timelimit: d, w, m. Defaults to None.
        max_results: max number of results. If None, returns results only from the first response. Defaults to None.

    Returns:
        List of dictionaries with news search results.
    """
    
    results = DDGS().news(
        keywords=keywords, 
        region=region, 
        safesearch=safesearch, 
        timelimit=timelimit, 
        max_results=max_results)

    return results

def function_wrapper(f):
    
    all_functions = []
    for function in f:
        sub_func = {}
        sub_func['type'] = "function"
        sub_func['function'] = function_to_json(function)
        all_functions.append(sub_func)
        
    return all_functions


def function_selection(function_name, function_args):
    
    if function_name == "text_search":
        result = text_search(**function_args)
    elif function_name == "pdf_search":
        result = pdf_search(**function_args)
    elif function_name == "image_search":
        result = image_search(**function_args)
    elif function_name ==  "video_search":
        result = video_search(**function_args)
    elif function_name ==  "news_search":
        result = news_search(**function_args)
    else:
        raise ValueError("There is no function with name of {}".format(function_name))
    
    return result
