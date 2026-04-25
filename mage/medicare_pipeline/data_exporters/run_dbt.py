import subprocess
import logging

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

DBT_PROJECT_DIR = '/home/src/medicare_insights'
DBT_PROFILES_DIR = '/home/src/medicare_insights'

logger = logging.getLogger(__name__)


@data_exporter
def run_dbt_transformations(data, *args, **kwargs):
    commands = [
        ['dbt', 'deps', '--project-dir', DBT_PROJECT_DIR, '--profiles-dir', DBT_PROFILES_DIR],
        ['dbt', 'run',  '--project-dir', DBT_PROJECT_DIR, '--profiles-dir', DBT_PROFILES_DIR],
        ['dbt', 'test', '--project-dir', DBT_PROJECT_DIR, '--profiles-dir', DBT_PROFILES_DIR],
    ]

    for cmd in commands:
        logger.info('Running: %s', ' '.join(cmd))
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.stdout:
            logger.info(result.stdout)
        if result.stderr:
            logger.warning(result.stderr)

        if result.returncode != 0:
            raise RuntimeError(
                f"dbt command failed: {' '.join(cmd)}\n{result.stderr}"
            )

    logger.info('dbt run and test completed successfully.')
