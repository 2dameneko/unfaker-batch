# unfaker-batch

A Python script for batch processing images (or single images) into optimized pixel art using the powerful [unfake.py](https://github.com/painebenjamin/unfake.py) library. This tool adds convenient batch processing capabilities and automatic 8x nearest-neighbor upscaling for better previewing, making it easy to convert entire folders of AI-generated or other images into clean, retro-style pixel art.

## Features

*   **Batch Processing:** Convert entire folders of images with a single command.
*   **Full `unfake.py` Compatibility:** Supports all command-line options from the core `unfake` library for precise control over the pixel art conversion process (scale detection, color quantization, downscaling methods, cleanup, etc.).
*   **Automatic Upscaling:** Generates a second output file for each image, upscaled 8x using nearest-neighbor interpolation for easy viewing and comparison.
*   **Flexible Output:** By default, saves the main processed image as a `.png` and the upscaled version with the original file extension (if suitable) or `.png`. Offers an option (`--no-save-main`) to save *only* the upscaled version.
*   **Easy to Use:** Simple command-line interface.

## Installation

1.  **Download `unfaker-batch`:** Clone this repository.
2.  **Install:** 
    ```bash
    pip install -r requirements.txt
    ```
    This will also install necessary dependencies like Pillow and unfake.

## Usage

```bash
python unfaker-batch.py <input> [options]
```

### Arguments

*   `input`: Path to the input image file or a directory containing images to process.

### Options

*   `-o PREFIX`, `--output-prefix PREFIX`: Prefix for output filenames (default: `pixelart_`).
*   `-u SUFFIX`, `--upscaled-suffix SUFFIX`: Suffix for the upscaled output filename (default: `_8x`).
*   `--upscale-only`: Only perform 8x nearest neighbor upscale, skip `unfake` processing.
*   `--no-save-main`: Do not save the main `unfake` processed image, only the upscaled one.
*   `-c COLORS`, `--colors COLORS`: Maximum number of colors (default: auto-detect).
*   `--auto-colors`: Auto-detect optimal color count.
*   `-s SCALE`, `--scale SCALE`: Manual scale override.
*   `-d {auto,runs,edge}`, `--detect {auto,runs,edge}`: Scale detection method (default: `auto`).
*   `-m {dominant,median,mode,mean,nearest,content-adaptive}`, `--method {dominant,median,mode,mean,nearest,content-adaptive}`: Downscaling method (default: `dominant`).
*   `--threshold THRESHOLD`: Dominant color threshold (default: `0.05`).
*   `--cleanup CLEANUP`: Cleanup options: `morph`, `jaggy` (comma-separated).
*   `--palette PALETTE`: Fixed palette file (hex colors, one per line).
*   `--alpha-threshold ALPHA_THRESHOLD`: Alpha binarization threshold (default: `128`).
*   `--no-snap`: Disable grid snapping.
*   `-q`, `--quiet`: Suppress output.
*   `-v`, `--verbose`: Verbose output.
*   `-h`, `--help`: Show help message and exit.

### Examples

*   **Process a single image with default settings:**
    ```bash
    python unfaker-batch.py my_image.jpg
    ```
    *Output:* `pixelart_my_image.png` (processed), `pixelart_my_image_8x.png` (upscaled)

*   **Process a folder of images with 16 colors using the median method:**
    ```bash
    python unfaker-batch.py ./my_images/ -c 16 -m median
    ```

*   **Process an image with a fixed palette:**
    ```bash
    python unfaker-batch.py input.png --palette my_colors.txt
    ```
    *(Assuming `my_colors.txt` contains hex colors like `#FF0000`, `#00FF00`, etc.)*

*   **Only save the upscaled versions:**
    ```bash
    python unfaker-batch.py input_folder/ --no-save-main
    ```

*   **Force a specific scale (e.g., 8x) and use edge detection:**
    ```bash
    python unfaker-batch.py image.png --scale 4 --detect edge
    ```

*   **Apply morphological cleanup and disable grid snapping:**
    ```bash
    python unfaker-batch.py image.png --cleanup morph --no-snap
    ```

## Credits

This project utilizes and builds upon the excellent work of others:

*   **[unfake.py](https://github.com/painebenjamin/unfake.py):** The core Python library used for pixel art optimization. A Python port by Benjamin Paine.
*   **[unfake.js](https://github.com/jenissimo/unfake.js):** The original JavaScript implementation by Eugeniy Smirnov ([@jenissimo](https://github.com/jenissimo)) that `unfake.py` is based on.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.