from extract import extract_data
from transform import transform_data
from quality_checks import run_quality_checks
from load import load_data

if __name__ == "__main__":

    appearances, clubs = extract_data()

    print("Appearances rows:", len(appearances))
    print("Clubs rows:", len(clubs))

    transformed_data = transform_data(appearances, clubs)

    print("Transformed rows:", len(transformed_data))

    run_quality_checks(transformed_data)

    load_data(transformed_data)

    print("Pipeline completed successfully")
