call venv\Scripts\activate
python unfaker-batch.py --colors 128 --pre-filter --edge-preserve --no-save-main --cleanup morph,jaggy %1
rem --method content-adaptive 
rem --method hybrid
rem --method dominant
rem --pre-filter --edge-preserve 