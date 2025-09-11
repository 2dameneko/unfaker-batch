"""
Advanced Pixel Art Converter using unfake.py

This script processes images or folders of images using the unfake library
to optimize them as pixel art. It supports all unfake options and adds
8x nearest-neighbor upscaling for better viewing.

Usage:
  python pixelart_converter.py <input> [options]

Arguments:
  input                 Input image file or folder.

Options:
  -o PREFIX, --output-prefix PREFIX
                        Prefix for output filenames (default: 'pixelart_').
  -u SUFFIX, --upscaled-suffix SUFFIX
                        Suffix for the upscaled output filename (default: '_8x').
  --upscale-only        Only perform 4x nearest neighbor upscale, skip unfake processing.
  --no-save-main        Do not save the main unfaked processed image.
  --no-save-upscaled    Do not save the upscaled unfaked processed image.
  -c COLORS, --colors COLORS
                        Maximum number of colors (default: auto-detect).
  --auto-colors         Auto-detect optimal color count.
  -s SCALE, --scale SCALE
                        Manual scale override.
  -d {auto,runs,edge}, --detect {auto,runs,edge}
                        Scale detection method (default: auto).
  -m {dominant,median,mode,mean,nearest,content-adaptive}, --method {dominant,median,mode,mean,nearest,content-adaptive}
                        Downscaling method (default: dominant).
  --threshold THRESHOLD
                        Dominant color threshold (default: 0.05).
  --cleanup CLEANUP     Cleanup options: morph,jaggy (comma-separated).
  --palette PALETTE     Fixed palette file (hex colors, one per line).
  --alpha-threshold ALPHA_THRESHOLD
                        Alpha binarization threshold (default: 128).
  --no-snap             Disable grid snapping.
  -q, --quiet           Suppress output.
  -v, --verbose         Verbose output.
  -h, --help            Show this help message and exit.
"""

import argparse
import logging
import os
import sys
from pathlib import Path
from typing import List, Optional, Tuple

# --- Import unfake ---
try:
    import unfake
    from PIL import Image
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Please ensure 'unfake' and 'Pillow' are installed.")
    print("pip install unfake Pillow")
    sys.exit(1)

# Configure logging based on unfake's logger
logger = logging.getLogger("pixelart_converter")


def get_image_files(input_path: str) -> List[Path]:
    """Get a list of image files from a path (file or folder)."""
    input_p = Path(input_path)
    if input_p.is_file():
        # Check if it's a common image format
        if input_p.suffix.lower() in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif', '.webp']:
             return [input_p]
        else:
             logger.warning(f"File '{input_p}' might not be a standard image format. Attempting processing anyway.")
             return [input_p] # Let unfake handle potential errors
    elif input_p.is_dir():
        # Common image extensions
        extensions = ('*.png', '*.jpg', '*.jpeg', '*.bmp', '*.tiff', '*.tif', '*.webp')
        files = []
        for ext in extensions:
            files.extend(input_p.glob(ext))
        # Also check for uppercase extensions
        for ext in extensions:
            files.extend(input_p.glob(ext.upper()))
        return sorted(list(set(files))) # Remove potential duplicates
    else:
        logger.error(f"Input path '{input_path}' is neither a file nor a directory.")
        return []


def upscale_nearest_neighbor(input_image: Image.Image, scale: int = 8) -> Image.Image:
    """Performs nearest neighbor upscaling."""
    try:
        width, height = input_image.size
        new_size = (width * scale, height * scale)
        upscaled_image = input_image.resize(new_size, Image.NEAREST)
        return upscaled_image
    except Exception as e:
        logger.error(f"Error during upscaling: {e}")
        raise


def process_single_image(
    input_file: Path,
    args: argparse.Namespace,
    cleanup_options: dict,
    fixed_palette: Optional[List[str]]
) -> bool:
    """Process a single image file."""
    try:
        logger.info(f"--- Processing '{input_file}' ---")

        # --- 1. Run unfake processing (unless upscale-only) ---
        if not args.upscale_only:
            unfake_kwargs = {
                "max_colors": args.colors,
                "manual_scale": args.scale,
                "detect_method": args.detect,
                "downscale_method": args.method,
                "dom_mean_threshold": args.threshold,
                "cleanup": cleanup_options,
                "fixed_palette": fixed_palette,
                "alpha_threshold": args.alpha_threshold,
                "snap_grid": not args.no_snap,
                "auto_color_detect": args.auto_colors,
            }

            # Filter out None values to let unfake use its defaults
            unfake_kwargs = {k: v for k, v in unfake_kwargs.items() if v is not None}

            logger.debug(f"unfake arguments: {unfake_kwargs}")
            result = unfake.process_image_sync(str(input_file), **unfake_kwargs)

            # --- 2. Save the unfake processed image (as PNG) ---
            processed_pil_image = result['image']
            base_name = input_file.stem
            # Force output extension to .png for the main file
            output_ext_main = ".png"

            output_filename_main = f"{args.output_prefix}{base_name}{output_ext_main}"
            output_path_main = input_file.parent / output_filename_main

            # Handle potential alpha issues if original was JPEG but output is PNG
            # (Less critical now as we always save as PNG, but good practice)
            # if processed_pil_image.mode == 'RGBA' and input_file.suffix.lower() in ['.jpg', '.jpeg']:
            #      logger.info(f"Processed image is RGBA, original was JPEG. Saving as RGBA PNG: {output_path_main}")

            if not args.no_save_main:
                processed_pil_image.save(output_path_main)
                logger.info(f"Saved unfake processed image (PNG) to '{output_path_main}'")
            else:
                 logger.info(f"Skipping save of main unfake processed image (--no-save-main).")

            if not args.no_save_upscaled:
                  # --- 3. Upscale the unfake processed image ---
                upscaled_image = upscale_nearest_neighbor(processed_pil_image, 8)

                # Determine upscaled file extension (use original if it's a common one that supports alpha, otherwise PNG)
                original_ext = input_file.suffix.lower()
                if original_ext in ['.png', '.tiff', '.tif']:
                    output_ext_upscaled = original_ext
                else: # Default to PNG for upscaled if original format is lossy or doesn't handle alpha well for our use case
                    output_ext_upscaled = ".png" # Or keep as original_ext if you prefer, but PNG is safer for transparency.

                output_filename_upscaled = f"{args.output_prefix}{base_name}{args.upscaled_suffix}{output_ext_upscaled}"
                output_path_upscaled = input_file.parent / output_filename_upscaled
                upscaled_image.save(output_path_upscaled)
                logger.info(f"Saved 8x upscaled image to '{output_path_upscaled}'")
            else:
                 logger.info(f"Skipping save of upscaled unfake processed image (--no-save-upscale).")                  

        # --- 4. If upscale-only, upscale the original ---
        else:
            logger.info("Upscale-only mode selected.")
            # Load the original image
            with Image.open(input_file) as original_image:
                # Convert if necessary for consistency (though NEAREST resize usually handles it)
                if original_image.mode not in ("RGB", "RGBA"):
                     original_image = original_image.convert("RGBA")

                # Determine upscaled file extension
                original_ext = input_file.suffix.lower()
                if original_ext in ['.png', '.tiff', '.tif', '.webp']:
                     output_ext_upscaled = original_ext
                else:
                     output_ext_upscaled = ".png"

                upscaled_image = upscale_nearest_neighbor(original_image, 8)

            base_name = input_file.stem
            output_filename_upscaled = f"{args.output_prefix}{base_name}{args.upscaled_suffix}{output_ext_upscaled}"
            output_path_upscaled = input_file.parent / output_filename_upscaled
            upscaled_image.save(output_path_upscaled)
            logger.info(f"Saved 4x upscaled (original) image to '{output_path_upscaled}'")

        logger.info(f"Finished processing '{input_file}'\n")
        return True

    except Exception as e:
        logger.error(f"Failed to process '{input_file}': {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return False


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Advanced Pixel Art Converter using unfake.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__[__doc__.find("Usage:"):], # Include usage in help
    )
    parser.add_argument("input", help="Input image file or folder.")
    parser.add_argument(
        "-o", "--output-prefix",
        default="pixelart_",
        help="Prefix for output filenames (default: 'pixelart_')."
    )
    parser.add_argument(
        "-u", "--upscaled-suffix",
        default="_8x",
        help="Suffix for the upscaled output filename (default: '_8x')."
    )
    parser.add_argument(
        "--upscale-only",
        action="store_true",
        help="Only perform 8x nearest neighbor upscale, skip unfake processing."
    )
    # Argument for saving the main file
    parser.add_argument(
        "-nsm", "--no-save-main",
        dest='no_save_main', # Name of the attribute
        action='store_true',
        default=False, # Default is False
        help="Do not save the main unfaked processed image. (default: False)."
    )
    parser.add_argument(
        "-nsu", "--no-save-upscaled",
        dest='no_save_upscaled', # Name of the attribute
        action='store_true',
        default=False, # Default is False
        help="Do not save the upscaled unfaked processed image. (default: False)."
    )
    # Arguments passed directly to unfake
    parser.add_argument(
        "-c", "--colors", type=int, help="Maximum number of colors (default: auto-detect)"
    )
    parser.add_argument(
        "--auto-colors", action="store_true", help="Auto-detect optimal color count"
    )
    parser.add_argument("-s", "--scale", type=int, help="Manual scale override")
    parser.add_argument(
        "-d",
        "--detect",
        choices=["auto", "runs", "edge"],
        default="auto",
        help="Scale detection method (default: auto)",
    )
    parser.add_argument(
        "-m",
        "--method",
        choices=["dominant", "median", "mode", "mean", "nearest", "content-adaptive"],
        default="dominant",
        help="Downscaling method (default: dominant)",
    )
    parser.add_argument(
        "--threshold", type=float, default=0.05, help="Dominant color threshold (default: 0.05)"
    )
    parser.add_argument("--cleanup", help="Cleanup options: morph,jaggy (comma-separated)")
    parser.add_argument("--palette", help="Fixed palette file (hex colors, one per line)")
    parser.add_argument(
        "--alpha-threshold",
        type=int,
        default=128,
        help="Alpha binarization threshold (default: 128)",
    )
    parser.add_argument("--no-snap", action="store_true", help="Disable grid snapping")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress output")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    # --- Set logging level ---
    if args.quiet:
        logging.getLogger().setLevel(logging.ERROR)
        # Suppress unfake's output too if quiet
        logging.getLogger("unfake.py").setLevel(logging.ERROR)
    elif args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger("unfake.py").setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)
        # Default unfake logging level is INFO, which is fine

    # --- Parse cleanup options ---
    cleanup_options = {"morph": False, "jaggy": False}
    if args.cleanup:
        for option in args.cleanup.split(","):
            option = option.strip().lower()
            if option in cleanup_options:
                cleanup_options[option] = True
            else:
                print(f"Warning: Unknown cleanup option '{option}'")

    # --- Load fixed palette if specified ---
    fixed_palette = None
    if args.palette:
        try:
            with open(args.palette) as f:
                # Strip whitespace and filter lines starting with #
                fixed_palette = [line.strip() for line in f if line.strip().startswith("#")]
            if not fixed_palette:
                 logger.warning(f"No valid hex colors found in palette file '{args.palette}'. Ignoring palette.")
                 fixed_palette = None
            else:
                 logger.info(f"Loaded palette with {len(fixed_palette)} colors from '{args.palette}'")
        except FileNotFoundError:
            logger.error(f"Error: Palette file '{args.palette}' not found")
            sys.exit(1)
        except Exception as e:
             logger.error(f"Error reading palette file '{args.palette}': {e}")
             sys.exit(1)


    # --- Get list of files to process ---
    image_files = get_image_files(args.input)
    if not image_files:
        logger.error("No valid image files found to process.")
        sys.exit(1)

    logger.info(f"Found {len(image_files)} image file(s) to process.")

    # --- Process each file ---
    success_count = 0
    for img_file in image_files:
        if process_single_image(img_file, args, cleanup_options, fixed_palette):
            success_count += 1

    logger.info(f"--- Processing Complete ---")
    logger.info(f"Successfully processed {success_count}/{len(image_files)} file(s).")

    if success_count != len(image_files):
        sys.exit(1) # Exit with error code if any failed


if __name__ == "__main__":
    main()