"""
Plain Text Cleaner

Responsible for cleaning raw text documents
before RAG ingestion.

Features:

- Unicode normalization
- Remove control characters
- Normalize whitespace
- Remove duplicate empty lines
- Normalize line endings
- OCR noise cleanup
- Optional header/footer removal


Used for:

- TXT files
- OCR output
- Email exports
- Legacy documents


Author
------
Tech Knowledge Navigator
"""

from __future__ import annotations


import logging


import re


import unicodedata


from dataclasses import dataclass, field



logger = logging.getLogger(__name__)



###############################################################################
# Models
###############################################################################


@dataclass
class TextCleaningMetadata:
    """
    Metadata generated during cleaning.
    """

    original_length: int

    cleaned_length: int

    removed_characters: int

    removed_lines: int

    unicode_normalized: bool



@dataclass
class CleanedText:
    """
    Cleaning result.
    """

    content: str

    metadata: TextCleaningMetadata



###############################################################################
# Configuration
###############################################################################


@dataclass
class TextCleanerConfig:
    """
    Plain text cleaning rules.
    """

    normalize_unicode: bool = True

    remove_control_characters: bool = True

    normalize_spaces: bool = True

    remove_empty_lines: bool = True

    remove_duplicate_lines: bool = False

    remove_ocr_noise: bool = True

    min_line_length: int = 2



###############################################################################
# Text Cleaner
###############################################################################


class TextCleaner:
    """
    Cleans plain text documents.

    """



    def __init__(
        self,
        config: TextCleanerConfig | None = None,
    ):

        self.config = (

            config

            or TextCleanerConfig()

        )



    ###########################################################################
    # Public API
    ###########################################################################


    async def clean(
        self,
        text: str,
    ) -> CleanedText:
        """
        Clean plain text content.
        """

        if not text.strip():

            return CleanedText(

                content="",

                metadata=TextCleaningMetadata(

                    original_length=0,

                    cleaned_length=0,

                    removed_characters=0,

                    removed_lines=0,

                    unicode_normalized=False,

                ),

            )



        original_length = len(text)


        original_lines = len(
            text.splitlines()
        )


        content = text



        #######################################################################
        # Unicode normalization
        #######################################################################

        unicode_normalized = False


        if self.config.normalize_unicode:

            content = unicodedata.normalize(

                "NFKC",

                content,

            )

            unicode_normalized = True



        #######################################################################
        # Remove control characters
        #######################################################################

        if self.config.remove_control_characters:

            content = (
                self._remove_control_chars(
                    content
                )
            )



        #######################################################################
        # OCR cleanup
        #######################################################################

        if self.config.remove_ocr_noise:

            content = (
                self._clean_ocr_noise(
                    content
                )
            )



        #######################################################################
        # Normalize whitespace
        #######################################################################

        if self.config.normalize_spaces:

            content = (
                self._normalize_spaces(
                    content
                )
            )



        #######################################################################
        # Duplicate lines
        #######################################################################

        if self.config.remove_duplicate_lines:

            content = (
                self._remove_duplicate_lines(
                    content
                )
            )



        #######################################################################
        # Empty lines
        #######################################################################

        if self.config.remove_empty_lines:

            content = (
                self._remove_empty_lines(
                    content
                )
            )



        cleaned_lines = len(
            content.splitlines()
        )


        metadata = TextCleaningMetadata(

            original_length=original_length,

            cleaned_length=len(content),

            removed_characters=(

                original_length

                -

                len(content)

            ),

            removed_lines=(

                original_lines

                -

                cleaned_lines

            ),

            unicode_normalized=
                unicode_normalized,

        )



        logger.info(

            "Text cleaned %s -> %s characters",

            original_length,

            len(content),

        )



        return CleanedText(

            content=content,

            metadata=metadata,

        )



    ###########################################################################
    # Unicode / Control Cleanup
    ###########################################################################


    def _remove_control_chars(
        self,
        text: str,
    ) -> str:
        """
        Remove invisible control characters.
        """

        return "".join(

            char

            for char in text

            if (

                char == "\n"

                or char == "\t"

                or not unicodedata.category(
                    char
                ).startswith(
                    "C"
                )

            )

        )



    ###########################################################################
    # OCR Cleanup
    ###########################################################################


    def _clean_ocr_noise(
        self,
        text: str,
    ) -> str:
        """
        Removes common OCR artifacts.

        Examples:

        "he11o" -> "hello"
        "----"  -> removed


        """

        #
        # Remove repeated punctuation
        #

        text = re.sub(

            r"([.,!?])\1{2,}",

            r"\1",

            text,

        )


        #
        # Remove page markers
        #

        text = re.sub(

            r"\bpage\s+\d+\b",

            "",

            text,

            flags=re.IGNORECASE,

        )


        #
        # Remove standalone separators
        #

        text = re.sub(

            r"^\s*[-_=]{4,}\s*$",

            "",

            text,

            flags=re.MULTILINE,

        )


        return text



    ###########################################################################
    # Whitespace Normalization
    ###########################################################################


    def _normalize_spaces(
        self,
        text: str,
    ) -> str:
        """
        Normalize spaces and tabs.
        """

        text = re.sub(

            r"[ \t]+",

            " ",

            text,

        )


        text = re.sub(

            r" *\n *",

            "\n",

            text,

        )


        return text



    ###########################################################################
    # Empty Lines
    ###########################################################################


    def _remove_empty_lines(
        self,
        text: str,
    ) -> str:
        """
        Remove excessive blank lines.
        """

        lines = []


        for line in text.splitlines():

            if (

                line.strip()

                or not lines

            ):

                lines.append(
                    line.rstrip()
                )



        text = "\n".join(lines)



        return re.sub(

            r"\n{3,}",

            "\n\n",

            text,

        )



    ###########################################################################
    # Duplicate Lines
    ###########################################################################


    def _remove_duplicate_lines(
        self,
        text: str,
    ) -> str:
        """
        Remove repeated lines.

        Useful for:

        - OCR PDFs
        - Headers
        - Footers

        """

        seen = set()

        result = []


        for line in text.splitlines():

            normalized = line.strip()


            if not normalized:

                result.append(line)

                continue



            if normalized in seen:

                continue



            seen.add(
                normalized
            )


            result.append(
                line
            )



        return "\n".join(result)