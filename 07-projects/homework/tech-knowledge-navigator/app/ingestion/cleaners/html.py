"""
HTML Content Cleaner

Responsible for converting raw HTML documents
into clean text suitable for RAG ingestion.

Features:

- Remove scripts
- Remove styles
- Remove navigation elements
- Remove hidden content
- Extract readable text
- Normalize whitespace
- Preserve headings

Used by:

- Web crawler ingestion
- Knowledge base ingestion
- Documentation ingestion


Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations


import logging


import re


from dataclasses import dataclass, field


from typing import Protocol


logger = logging.getLogger(__name__)



###############################################################################
# Optional HTML Parser Contract
###############################################################################


class HTMLParser(Protocol):
    """
    HTML parser abstraction.

    Possible implementations:

    - BeautifulSoup
    - lxml
    - selectolax

    """

    def remove_tags(
        self,
        html: str,
        tags: list[str],
    ) -> str:
        ...


    def extract_text(
        self,
        html: str,
    ) -> str:
        ...



###############################################################################
# Models
###############################################################################


@dataclass
class HTMLCleaningMetadata:
    """
    Metadata generated during cleaning.
    """

    original_length: int

    cleaned_length: int

    removed_characters: int

    removed_tags: list[str] = field(
        default_factory=list
    )



@dataclass
class CleanedHTML:
    """
    Cleaning output.
    """

    content: str

    metadata: HTMLCleaningMetadata



###############################################################################
# Configuration
###############################################################################


@dataclass
class HTMLCleanerConfig:
    """
    HTML cleaning rules.
    """

    remove_scripts: bool = True

    remove_styles: bool = True

    remove_navigation: bool = True

    remove_comments: bool = True

    preserve_links: bool = False



    ignored_tags: list[str] = field(

        default_factory=lambda: [

            "script",

            "style",

            "noscript",

            "svg",

            "iframe",

            "canvas",

            "footer",

        ]

    )


    navigation_tags: list[str] = field(

        default_factory=lambda: [

            "nav",

            "header",

            "menu",

            "aside",

        ]

    )



###############################################################################
# HTML Cleaner
###############################################################################


class HTMLCleaner:
    """
    Cleans HTML content for RAG ingestion.

    Pipeline:

    Raw HTML

        |
        v

    Remove unwanted tags

        |
        v

    Extract text

        |
        v

    Normalize whitespace

        |
        v

    Clean text


    """



    def __init__(
        self,
        parser: HTMLParser,
        config: HTMLCleanerConfig | None = None,
    ):

        self.parser = parser


        self.config = (

            config

            or HTMLCleanerConfig()

        )



    ###########################################################################
    # Public API
    ###########################################################################


    async def clean(
        self,
        html: str,
    ) -> CleanedHTML:
        """
        Clean HTML document.

        """

        if not html.strip():

            return CleanedHTML(

                content="",

                metadata=HTMLCleaningMetadata(

                    original_length=0,

                    cleaned_length=0,

                    removed_characters=0,

                ),

            )



        original_length = len(html)


        removed_tags = []



        cleaned_html = html



        #######################################################################
        # Remove scripts/styles
        #######################################################################

        if self.config.remove_scripts:

            cleaned_html = (
                self.parser.remove_tags(

                    cleaned_html,

                    [
                        "script"
                    ],

                )
            )


            removed_tags.append(
                "script"
            )



        if self.config.remove_styles:

            cleaned_html = (
                self.parser.remove_tags(

                    cleaned_html,

                    [
                        "style"
                    ],

                )
            )


            removed_tags.append(
                "style"
            )



        #######################################################################
        # Remove navigation
        #######################################################################

        if self.config.remove_navigation:

            cleaned_html = (
                self.parser.remove_tags(

                    cleaned_html,

                    self.config.navigation_tags,

                )
            )


            removed_tags.extend(

                self.config.navigation_tags

            )



        #######################################################################
        # Remove ignored elements
        #######################################################################

        cleaned_html = (
            self.parser.remove_tags(

                cleaned_html,

                self.config.ignored_tags,

            )
        )



        #######################################################################
        # Extract text
        #######################################################################

        text = (
            self.parser.extract_text(
                cleaned_html
            )
        )



        #######################################################################
        # Normalize
        #######################################################################

        text = self._normalize(
            text
        )



        metadata = HTMLCleaningMetadata(

            original_length=original_length,

            cleaned_length=len(text),

            removed_characters=(

                original_length

                -
                
                len(text)

            ),

            removed_tags=removed_tags,

        )



        logger.info(

            "HTML cleaned %s -> %s characters",

            original_length,

            len(text),

        )



        return CleanedHTML(

            content=text,

            metadata=metadata,

        )



    ###########################################################################
    # Text Normalization
    ###########################################################################


    def _normalize(
        self,
        text: str,
    ) -> str:
        """
        Normalize extracted text.

        """

        # Remove multiple spaces

        text = re.sub(

            r"[ \t]+",

            " ",

            text,

        )


        # Normalize new lines

        text = re.sub(

            r"\n\s*\n\s*\n+",

            "\n\n",

            text,

        )


        # Remove leading/trailing spaces

        return text.strip()