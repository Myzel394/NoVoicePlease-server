import logging
import traceback

try:
    import spleeter
    from spleeter.separator import Separator
except ImportError:
    logging.error("=" * 200 + "\nCouldn't load Spleeter." + "=" * 200)
    traceback.print_exc()

try:
    import librosa
except ImportError:
    logging.error("=" * 200 + "\nCouldn't load librosa." + "=" * 200)
    traceback.print_exc()
