# unfaker-batch

A Python script for batch processing images (or single images) into optimized pixel art using the enhanced fork [**unfake-opt.py**](https://github.com/2dameneko/unfake-opt.py) of the powerful [unfake.py](https://github.com/painebenjamin/unfake.py) library. This tool adds convenient batch processing capabilities and automatic **8× nearest-neighbor upscaling** for better previewing, making it easy to convert entire folders of AI-generated or other images into clean, retro-style pixel art.

## Features

- **Batch Processing**: Convert entire folders of images with a single command.
- **Use `unfake-opt.py` fork**: Supports all advanced options from the optimized core library, including:
  - `hybrid` downscaling
  - KMeans-enhanced `dominant` method
  - `--pre-filter`, `--edge-preserve`
  - Iterative threshold tuning (`--iterations`)
- **Automatic 8× Upscaling**: Generates a second output file for each image, upscaled using nearest-neighbor interpolation for crisp, zoomed previews.
- **Flexible Output Control**:
  - Save only the processed image (`--no-save-upscaled`)
  - Save only the upscaled version (`--no-save-main`)
  - Customize output filename prefixes and suffixes
- **Easy to Use**: Simple command-line interface with helpful defaults.

## Installation

1. **Clone this repository** (which includes `unfaker-batch.py`):
   ```bash
   git clone https://github.com/2dameneko/unfaker-batch.git
   cd unfaker-batch
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   > This installs a pre-built wheel of `unfake-opt.py` (compiled for **Windows x64, Python 3.10**), along with Pillow and other required packages.

> 💡 **Note**: If you're using a different operating system, Python version, or architecture (e.g., Linux, macOS, Python 3.11+, ARM64), the pre-built wheel may not be compatible. In that case, you can clone the [`unfake-opt.py`](https://github.com/2dameneko/unfake-opt.py) repository and build the package from source. This requires a **Rust compiler** (install via [rustup](https://rustup.rs/)) and will compile the optimized Rust extensions during installation.

## Usage

```bash
python unfaker-batch.py <input> [options]
```

### Arguments

- `input`: Path to an input image file **or** a folder containing images.

### Options

#### Output Control
- `-o PREFIX`, `--output-prefix PREFIX`: Prefix for output filenames (default: `pixelart_`).
- `-u SUFFIX`, `--upscaled-suffix SUFFIX`: Suffix for upscaled filename (default: `_8x`).
- `--no-save-main`: Skip saving the main (`unfake`-processed) image.
- `--no-save-upscaled`: Skip saving the 8× upscaled version.
- `--upscale-only`: Skip `unfake` processing entirely; only perform 8× nearest-neighbor upscale of the original.

#### Pixel Art Processing (passed to `unfake-opt.py`)
- `-c COLORS`, `--colors COLORS`: Maximum number of colors (default: auto-detect).
- `--auto-colors`: Enable automatic optimal color count detection.
- `-s SCALE`, `--scale SCALE`: Manually override detected scale (e.g., `4` for 4× downscale).
- `-d {auto,runs,edge}`, `--detect {auto,runs,edge}`: Scale detection method (default: `auto`).
- `-m {dominant,median,mode,mean,nearest,content-adaptive,hybrid}`, `--method METHOD`: Downscaling method (default: `dominant`).  
  > ✨ **New**: `hybrid` intelligently combines `dominant` and `content-adaptive` per block.
- `--threshold THRESHOLD`: Dominant color threshold (0.0–1.0, default: `0.05`).
- `--iterations ITERATIONS`: Number of refinement iterations for threshold tuning (default: `1`).
- `--cleanup CLEANUP`: Enable cleanup steps: `morph`, `jaggy` (comma-separated, e.g., `--cleanup morph,jaggy`).
- `--palette PALETTE`: Path to a `.txt` file with fixed hex colors (one per line, e.g., `#FF0000`).
- `--alpha-threshold ALPHA_THRESHOLD`: Threshold for alpha binarization (default: `128`).
- `--no-snap`: Disable automatic grid snapping.
- `--pre-filter`: Apply light blur before quantization to reduce noise.
- `--edge-preserve`: Enhance edge sharpness during downscaling.
- `--post-sharpen`: Apply experimental sharpening after quantization.

#### Logging
- `-q`, `--quiet`: Suppress all non-error output.
- `-v`, `--verbose`: Show detailed debug info (including `unfake` logs).

## Examples

- **Process a single image with defaults**:
  ```bash
  python unfaker-batch.py my_image.jpg
  ```
  → Outputs: `pixelart_my_image.png` (processed), `pixelart_my_image_8x.png` (upscaled)

- **Batch process a folder using the new `hybrid` method**:
  ```bash
  python unfaker-batch.py ai_outputs -m hybrid --edge-preserve
  ```

- **Use KMeans-enhanced dominant with iterative refinement**:
  ```bash
  python unfaker-batch.py image.png -m dominant --iterations 3 --pre-filter
  ```

- **Save only the upscaled version**:
  ```bash
  python unfaker-batch.py input.png --no-save-main
  ```

- **Apply fixed palette and disable grid snapping**:
  ```bash
  python unfaker-batch.py art.png --palette gameboy.txt --no-snap
  ```

- **Enable both cleanup passes**:
  ```bash
  python unfaker-batch.py image.png --cleanup morph,jaggy
  ```

## Versions

- **v0.2**: Switched to enhanced fork [unfake-opt.py](https://github.com/2dameneko/unfake-opt.py), added support for all new options (`hybrid`, `--pre-filter`, `--edge-preserve`, `--iterations`, etc.), and added `--no-save-upscaled`.
- **v0.1**: Initial release.

## Credits

This project builds upon excellent open-source work:

- **[unfake.js](https://github.com/jenissimo/unfake.js)** – Foundational JavaScript implementation by Eugeniy Smirnov.
- **[unfake.py](https://github.com/painebenjamin/unfake.py)** – Original Python port by Benjamin Paine.
- **[unfake-opt.py](https://github.com/2dameneko/unfake-opt.py)** – Optimized fork with Rust speedups and algorithmic improvements.

## License

MIT License – see the [LICENSE](LICENSE) file for details.
