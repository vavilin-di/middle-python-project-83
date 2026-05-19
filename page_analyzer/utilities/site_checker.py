__all__ = ["check_site"]

from re import I as CASE_INSENSITIVE
from re import compile as compile_regex

from bs4 import BeautifulSoup
from requests import get as get_request

from page_analyzer.schemas.url_checks import UrlCheckResult
from page_analyzer.schemas.urls import Url as UrlSchema


def check_site(url: UrlSchema) -> UrlCheckResult:
    url_string = str(url.name)
    response = get_request(url_string)
    response.raise_for_status()
    status_code = response.status_code

    soup = BeautifulSoup(response.text, "html.parser")
    title = "" if soup.title is None or soup.title.string is None else soup.title.string
    h1_tag = soup.find("h1")
    h1 = "" if h1_tag is None or h1_tag.string is None else h1_tag.string

    description_tag = soup.find("meta", attrs={"name": compile_regex(r"description", CASE_INSENSITIVE)})
    if description_tag is None:
        description = ""
    else:
        description_tag_content = description_tag.get("content")
        if description_tag_content is None:
            description = ""
        elif isinstance(description_tag_content, list):
            description = " ".join(description_tag_content)
        else:
            description = description_tag_content

    return UrlCheckResult(
        status_code=status_code,
        h1=h1,
        title=title,
        description=description,
    )
