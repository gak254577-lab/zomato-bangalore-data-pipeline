import logging
from src.extract import extract
from src.clean import clean
from src.transform import transform
from src.load import load
from src.analyze import analyze

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger("pipeline")

df = extract()
log.info("extracted: %d rows", len(df))
df = clean(df)
log.info("cleaned: %d rows", len(df))
df = transform(df)
log.info("transformed: %d rows", len(df))
log.info("loaded into database: %d rows", load(df))
analyze()