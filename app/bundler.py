from pathlib import Path
from typing import List, Optional, Union
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StaticBundler:
    DEFAULT_ENCODING = 'utf-8'
    FALLBACK_ENCODINGS = ['utf-8-sig', 'latin-1', 'iso-8859-1', 'cp1252']
    
    def __init__(
        self,
        template_path: Union[str, Path],
        scripts_dir: Union[str, Path],
        styles_dir: Union[str, Path],
        js_file_order: Optional[List[str]] = None,
        default_encoding: str = DEFAULT_ENCODING
    ):
        """
        Initialize the StaticBundler with paths to resources.
        
        Args:
            template_path: Path to the HTML template file
            scripts_dir: Directory containing JavaScript files
            styles_dir: Directory containing CSS files
            js_file_order: Custom order for JS files (glob patterns)
            default_encoding: Default encoding to use for file reading
        """
        self.template_path = Path(template_path)
        self.scripts_dir = Path(scripts_dir)
        self.styles_dir = Path(styles_dir)
        self.js_file_order = js_file_order or [
            "const.js",
            "state.js",
            "utils/*.js",
            "services/*.js",
            "ui-helper.js",
            "init.js",
            "main.js"
        ]
        self.default_encoding = default_encoding

    def _read_files(self, dir_path: Path, patterns: List[str]) -> List[Path]:
        """
        Get files from directory based on ordered glob patterns.
        
        Returns:
            List of Path objects for matching files
        """
        files = []
        seen_files = set()  # To avoid duplicates
        
        for pattern in patterns:
            try:
                for file_path in sorted(dir_path.glob(pattern)):
                    if file_path.is_file() and file_path not in seen_files:
                        files.append(file_path)
                        seen_files.add(file_path)
            except Exception as e:
                logger.warning(f"Error processing pattern '{pattern}' in {dir_path}: {e}")
                
        return files

    def _read_file_with_fallback_encodings(self, file_path: Path) -> str:
        """
        Attempt to read a file with multiple encodings.
        
        Args:
            file_path: Path to the file to read
            
        Returns:
            File content as string
            
        Raises:
            UnicodeDecodeError if all encoding attempts fail
        """
        encodings = [self.default_encoding] + self.FALLBACK_ENCODINGS
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logger.warning(f"Error reading {file_path} with encoding {encoding}: {e}")
                continue
                
        raise UnicodeDecodeError(
            f"Failed to decode {file_path} with attempted encodings: {encodings}"
        )

    def _read_file_content(self, file_path: Path, comment: str = None) -> str:
        """
        Read file content and optionally add a comment header.
        
        Args:
            file_path: Path to the file to read
            comment: Optional comment to prepend to the content
            
        Returns:
            File content as string, with optional comment
        """
        try:
            content = self._read_file_with_fallback_encodings(file_path)
            if comment:
                return f"\n\n/* {comment} */\n{content}"
            return content
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            return ""

    def bundle_js(self) -> str:
        """
        Bundle all JavaScript files in the specified order.
        
        Returns:
            Concatenated JavaScript content as string
        """
        js_files = self._read_files(self.scripts_dir, self.js_file_order)
        js_content = []
        
        for js_file in js_files:
            if js_file.suffix == ".js":
                js_content.append(self._read_file_content(js_file, js_file.name))
                
        return '\n'.join(js_content)

    def bundle_css(self) -> str:
        """
        Bundle all CSS files in alphabetical order.
        
        Returns:
            Concatenated CSS content as string
        """
        css_files = self._read_files(self.styles_dir, ["*.css"])
        css_content = []
        
        for css_file in css_files:
            if css_file.suffix == ".css":
                css_content.append(self._read_file_content(css_file, css_file.name))
                
        return '\n'.join(css_content)

    def generate_html(self) -> str:
        """
        Generate the final HTML with bundled JS and CSS.
        
        Returns:
            HTML content as string
            
        Raises:
            FileNotFoundError if template file is missing
            IOError if template cannot be read
        """
        try:
            html = self._read_file_with_fallback_encodings(self.template_path)
        except Exception as e:
            logger.error(f"Failed to read template file {self.template_path}: {e}")
            raise

        try:
            js_content = self.bundle_js()
            html = html.replace(
                '<script></script>',
                f'<script>\n{js_content}\n</script>'
            )
        except Exception as e:
            logger.error(f"Failed to bundle JavaScript: {e}")
            raise

        try:
            css_content = self.bundle_css()
            html = html.replace(
                '<style></style>',
                f'<style>\n{css_content}\n</style>'
            )
        except Exception as e:
            logger.error(f"Failed to bundle CSS: {e}")
            raise

        return html