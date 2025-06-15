import json
from io import BytesIO
from purrfectmeow import Malet, Kornja

from ...loggings import setup_logger

logger = setup_logger(__name__)

class ChunkingProcessor:

    @staticmethod
    def _select_loader(
        file_like: BytesIO,
        file_name: str,
        file_reader: str,
        extras: dict
    ) -> str:

        def make_loader(engine_name: str):
            return lambda: Malet.loader(file_like, file_name, loader=engine_name)

        loader_map = {
            "simple": {
                "default": "PYMUPDF",
                "engines": {
                    "PYMUPDF": make_loader("PYMUPDF"),
                    "PANDAS": make_loader("PANDAS")
                }
            },
            "ocr": {
                "default": "PYTESSERACT",
                "engines": {
                    "PYTESSERACT": make_loader("PYTESSERACT"),
                    "EASYOCR": make_loader("EASYOCR"),
                    "SURYAOCR": make_loader("SURYAOCR")
                }
            },
            "markdown": {
                "default": "MARKITDOWN",
                "engines": {
                    "MARKITDOWN": make_loader("MARKITDOWN"),
                    "DOCLING": make_loader("DOCLING")
                }
            }
        }

        config = loader_map.get(
            file_reader,
            {
                "default": None,
                "engines": {
                    None: make_loader("ENCODING")
                }
            }
        )

        loader_key = extras.get("loader_engine", config["default"])
        logger.info(f"Loader type: {file_reader}, engine: {loader_key}")

        loader_func = config["engines"].get(loader_key)
        logger.info(f"Loader function: {loader_func}")

        if loader_func:
            return loader_func()

        else:
            logger.info("Falling back to default loader")
            return Malet.loader(file_like, file_name, loader="ENCODING")


    @staticmethod
    def _apply_chunking(
        text: str,
        splitter: str,
        extras: dict
    ) -> list:

        chunk_params = {}

        if splitter == "token":
            logger.info("Applying `token` chunking strategy")

            chunk_params = {
                "splitter": "token",
                "chunk_size": extras.get(
                    "chunkSize", 
                    extras.get("chunk_size", 500)
                ),
                "chunk_overlap": extras.get(
                    "chunkOverlap", 
                    extras.get("chunk_overlap", 0)
                )
            }
            logger.info(f"Token chunking: size={chunk_params['chunk_size']}, overlap={chunk_params['chunk_overlap']}")

        elif splitter == "separator":
            logger.info("Applying `separator` chunking strategy")

            chunk_params = {
                "splitter": "separator",
                "separator": extras.get("separator", "\n\n")
            }
            logger.info(f"Separator chunking: separator={chunk_params['separator']}")

        else:
            logger.info("Applying `default` chunking strategy")
            
            if chunk_size := extras.get("chunkSize") or extras.get("chunk_size"):
                chunk_params = {
                    "splitter": "token",
                    "chunk_size": chunk_size,
                    "chunk_overlap": extras.get(
                        "chunkOverlap", 
                        extras.get("chunk_overlap", 0)
                    )
                }
                logger.info(f"Token chunking: size={chunk_size}, overlap={chunk_params['chunk_overlap']}")

            elif separator := extras.get("separator"):
                chunk_params = {
                    "splitter": "separator",
                    "separator": separator
                }
                logger.info(f"Separator chunking: separator={separator}")

            else:
                logger.info("Using fully default chunking strategy")

                return Kornja.chunking(text, **chunk_params)

        return Kornja.chunking(text, **chunk_params)

    @staticmethod
    def process_preview(
        file_like: BytesIO,
        file_name: str,
        file_reader: str,
        extra_params: dict
    ) -> list:
        logger.info("Starting process preview chunking...")
        extras = json.loads(extra_params) if extra_params else {}

        text = ChunkingProcessor._select_loader(
            file_like, 
            file_name, 
            file_reader, 
            extras
        )
        # logger.info(f"Text result from loading: {text}")
        chunks = ChunkingProcessor._apply_chunking(
            text, 
            extras.get("splitter", "token"), 
            extras
        )
        logger.info(f"Successfully chunked preview text into {len(chunks)} chunks.")
        return chunks