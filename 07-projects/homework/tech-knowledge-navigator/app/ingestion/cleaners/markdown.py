"""
Markdown Content Cleaner

Responsible for converting raw Markdown
documents into clean text suitable for RAG.

Features:

- Remove YAML front matter
- Remove markdown images
- Normalize links
- Preserve headings
- Remove excessive whitespace
- Clean code fences
- Preserve technical content

Used for:

- GitHub repositories
- Documentation sites
- Knowledge bases
- Technical articles


Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations


import logging


import re


from dataclasses import dataclass, field



logger = logging.getLogger(__name__)



###############################################################################
# Models
###############################################################################


@dataclass
class MarkdownCleaningMetadata:
    """
    Metadata generated during cleaning.
    """

    original_length: int

    cleaned_length: int

    removed_front_matter: bool

    removed_images: int

    removed_links: int



@dataclass
class CleanedMarkdown:
    """
    Cleaning result.
    """

    content: str

    metadata: MarkdownCleaningMetadata



###############################################################################
# Configuration
###############################################################################


@dataclass
class MarkdownCleanerConfig:
    """
    Markdown cleaning rules.
    """

    remove_front_matter: bool = True

    remove_images: bool = True

    simplify_links: bool = True

    preserve_code_blocks: bool = True

    remove_empty_lines: bool = True



###############################################################################
# Markdown Cleaner
###############################################################################


class MarkdownCleaner:
    """
    Cleans Markdown documents for RAG ingestion.

    Processing:

    Markdown
       |
       v
    Remove metadata
       |
       v
    Clean formatting
       |
       v
    Normalize text

    """



    def __init__(
        self,
        config: MarkdownCleanerConfig | None = None,
    ):

        self.config = (

            config

            or MarkdownCleanerConfig()

        )



    ###########################################################################
    # Public API
    ###########################################################################


    async def clean(
        self,
        markdown: str,
    ) -> CleanedMarkdown:
        """
        Clean markdown content.
        """

        if not markdown.strip():

            return CleanedMarkdown(

                content="",

                metadata=MarkdownCleaningMetadata(

                    original_length=0,

                    cleaned_length=0,

                    removed_front_matter=False,

                    removed_images=0,

                    removed_links=0,

                ),

            )



        original_length = len(markdown)


        content = markdown


        removed_front_matter = False



        #######################################################################
        # Remove YAML Metadata
        #######################################################################

        if self.config.remove_front_matter:

            content, removed_front_matter = (
                self._remove_front_matter(
                    content
                )
            )



        #######################################################################
        # Remove Images
        #######################################################################

        removed_images = 0


        if self.config.remove_images:

            content, removed_images = (
                self._remove_images(
                    content
                )
            )



        #######################################################################
        # Clean Links
        #######################################################################

        removed_links = 0


        if self.config.simplify_links:

            content, removed_links = (
                self._clean_links(
                    content
                )
            )



        #######################################################################
        # Normalize Content
        #######################################################################

        content = self._normalize(
            content
        )



        metadata = MarkdownCleaningMetadata(

            original_length=original_length,

            cleaned_length=len(content),

            removed_front_matter=
                removed_front_matter,

            removed_images=
                removed_images,

            removed_links=
                removed_links,

        )



        logger.info(

            "Markdown cleaned %s -> %s characters",

            original_length,

            len(content),

        )



        return CleanedMarkdown(

            content=content,

            metadata=metadata,

        )



    ###########################################################################
    # Front Matter Removal
    ###########################################################################


    def _remove_front_matter(
        self,
        text: str,
    ) -> tuple[str, bool]:
        """
        Remove YAML metadata.

        Example:

        ---
        title: Redis Guide
        author: Mahesh
        ---

        """

        pattern = (
            r"^---\s*\n.*?\n---\s*\n"
        )


        result, count = re.subn(

            pattern,

            "",

            text,

            flags=re.DOTALL,

        )


        return result, count > 0



    ###########################################################################
    # Image Removal
    ###########################################################################


    def _remove_images(
        self,
        text: str,
    ) -> tuple[str, int]:
        """
        Remove markdown images.

        Example:

        ![Architecture](image.png)

        """

        pattern = (
            r"!\[.*?\]\(.*?\)"
        )


        result, count = re.subn(

            pattern,

            "",

            text,

        )


        return result, count



    ###########################################################################
    # Link Cleaning
    ###########################################################################


    def _clean_links(
        self,
        text: str,
    ) -> tuple[str, int]:
        """
        Convert:

        [Redis Docs](https://redis.io)

        into:

        Redis Docs

        """

        pattern = (
            r"\[([^\]]+)\]\([^\)]+\)"
        )


        result, count = re.subn(

            pattern,

            r"\1",

            text,

        )


        return result, count



    ###########################################################################
    # Normalization
    ###########################################################################


    def _normalize(
        self,
        text: str,
    ) -> str:
        """
        Normalize markdown text.
        """

        #
        # Remove trailing spaces
        #

        text = re.sub(

            r"[ \t]+$",

            "",

            text,

            flags=re.MULTILINE,

        )



        #
        # Reduce excessive blank lines
        #

        if self.config.remove_empty_lines:

            text = re.sub(

                r"\n{3,}",

                "\n\n",

                text,

            )



        #
        # Remove markdown separators
        #

        text = re.sub(

            r"^\s*[-*_]{3,}\s*$",

            "",

            text,

            flags=re.MULTILINE,

        )



        return text.strip()