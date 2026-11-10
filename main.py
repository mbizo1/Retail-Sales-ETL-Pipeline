
from pathlib import Path
import subprocess
import sys
import logging

# ============================================================
# RETAIL SALES ETL - MAIN PIPELINE CONTROLLER
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
LOG_DIR = PROJECT_ROOT / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(
            LOG_DIR / "pipeline.log",
            encoding="utf-8"
        ),
        logging.StreamHandler(sys.stdout)
    ]
)

# Define pipeline execution order
PIPELINE_STEPS = [
    "extract.py",
    "transform.py",
    "load.py",
    "validate.py"
]


def run_pipeline():
    """Execute all ETL stages in sequence."""

    logging.info("Starting Retail Sales ETL Pipeline")

    for script in PIPELINE_STEPS:
        logging.info(f"Running {script}")

        subprocess.run(
            [sys.executable, str(SRC_DIR / script)],
            check=True,
            cwd=PROJECT_ROOT
        )

        logging.info(f"{script} completed successfully")

    logging.info("All ETL pipeline stages completed successfully!")


if __name__ == "__main__":
    try:
        run_pipeline()

    except subprocess.CalledProcessError as error:
        logging.error(
            f"Pipeline failed with exit code {error.returncode}"
        )
        sys.exit(1)

    except Exception:
        logging.exception("Unexpected pipeline error")
        sys.exit(1)
