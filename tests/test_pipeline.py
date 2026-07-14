from os.path import join

from hdx.utilities.downloader import Download
from hdx.utilities.path import temp_dir
from hdx.utilities.retriever import Retrieve

from hdx.scraper.idb.pipeline import Pipeline


class TestPipeline:
    def test_pipeline(self, configuration, fixtures_dir, input_dir, config_dir):
        with temp_dir(
            "TestIDB",
            delete_on_success=True,
            delete_on_failure=False,
        ) as tempdir:
            with Download(user_agent="test") as downloader:
                retriever = Retrieve(
                    downloader=downloader,
                    fallback_dir=tempdir,
                    saved_dir=input_dir,
                    temp_dir=tempdir,
                    save=False,
                    use_saved=True,
                )
                pipeline = Pipeline(configuration, retriever, tempdir)
                datasets = pipeline.generate_datasets()
                assert len(datasets) == 14

                dataset = datasets[0]
                dataset.update_from_yaml(
                    path=join(config_dir, "hdx_dataset_static.yaml")
                )
                assert dataset == {
                    "name": "idb-demographic-social-indicators",
                    "title": "Latin America and the Caribbean: Demographic social indicators",
                    "dataset_date": "[1990-01-01T00:00:00 TO 2025-01-01T23:59:59]",
                    "tags": [
                        {
                            "name": "population",
                            "vocabulary_id": "b891512e-9516-4bf5-962a-7a289772a2a1",
                        },
                        {
                            "name": "gender",
                            "vocabulary_id": "b891512e-9516-4bf5-962a-7a289772a2a1",
                        },
                    ],
                    "groups": [
                        {"name": "arg"},
                        {"name": "bhs"},
                        {"name": "jam"},
                        {"name": "pan"},
                        {"name": "ury"},
                        {"name": "ven"},
                        {"name": "brb"},
                        {"name": "per"},
                        {"name": "pri"},
                        {"name": "sur"},
                        {"name": "tto"},
                        {"name": "blz"},
                        {"name": "cri"},
                        {"name": "dom"},
                        {"name": "ecu"},
                        {"name": "bol"},
                        {"name": "bra"},
                        {"name": "chl"},
                        {"name": "col"},
                        {"name": "slv"},
                        {"name": "mex"},
                        {"name": "nic"},
                        {"name": "gtm"},
                        {"name": "guy"},
                        {"name": "hti"},
                        {"name": "hnd"},
                    ],
                    "notes": "The Social Indicators of Latin America and the Caribbean datasets offer a comprehensive view of social development trends across 21 countries in the region, spanning from 1990 to the present. This unique database compiles and standardizes social indicators using national household surveys, census data, and other validated sources, providing a robust foundation for regional comparisons.  \n  \nThis dataset includes the following indicators:  \n- Total population  \n- Percentage of men in population  \n- Percentage of women in population  \n- Percentage of the population under age 18 (Census)  \n- Percentage of population ages 65 and above (Census)",
                    "license_id": "cc-by",
                    "methodology": "Direct Observational Data/Anecdotal Data",
                    "caveats": "These indicators are not intended to serve as official statistics for individual countries, but rather to provide a standardized regional perspective.",
                    "dataset_source": "Inter-American Development Bank",
                    "package_creator": "HDX Data Systems Team",
                    "private": False,
                    "maintainer": "09842f0d-7005-4430-9675-9de547e68d84",
                    "owner_org": "2df1d0ff-527b-4707-8b10-6a87d0cdab26",
                    "data_update_frequency": 90,
                }

                resources = dataset.get_resources()
                assert resources == [
                    {
                        "name": "Percentage of men in population",
                        "description": "Percentage of men in population",
                        "url": "https://data.iadb.org/file/download/15adc7a1-a792-4158-9e1c-01af59efbc8f",
                        "format": "csv",
                    },
                    {
                        "name": "Percentage of women in population",
                        "description": "Percentage of women in population",
                        "url": "https://data.iadb.org/file/download/ae8777c6-83ac-4457-b1b9-a82a814a209e",
                        "format": "csv",
                    },
                    {
                        "name": "Total population",
                        "description": "Total population",
                        "url": "https://data.iadb.org/file/download/efd7fe33-f9b9-4109-bd2b-c0b0df4e023c",
                        "format": "csv",
                    },
                    {
                        "name": "Percentage of the population under age 18 (Census)",
                        "description": "Percentage of the population under 18 years of age (Census)",
                        "url": "https://data.iadb.org/file/download/4cf9b5ca-7e18-49f8-b15c-022fc7857bf9",
                        "format": "csv",
                    },
                    {
                        "name": "Percentage of population ages 65 and above (Census)",
                        "description": "Percentage population 65 years of age or older (Census)",
                        "url": "https://data.iadb.org/file/download/f3a76e7b-6e14-4274-840d-6e841de87407",
                        "format": "csv",
                    },
                ]
