#!/usr/bin/python
"""Idb scraper"""

import logging

from hdx.api.configuration import Configuration
from hdx.data.dataset import Dataset
from hdx.location.country import Country
from hdx.utilities.retriever import Retrieve
from slugify import slugify

logger = logging.getLogger(__name__)


class Pipeline:
    def __init__(self, configuration: Configuration, retriever: Retrieve, tempdir: str):
        self._configuration = configuration
        self._retriever = retriever
        self._tempdir = tempdir

    def generate_datasets(self) -> list[Dataset]:
        metadata = self._retriever.download_json(self._configuration["metadata_url"])
        metadata = metadata["result"]

        start_date = metadata["temporal_start"]
        end_date = metadata["temporal_end"]
        isos = []
        for location in metadata["spatial_coverage"]:
            country_name = location["label"]["en"]
            iso, _ = Country.get_iso3_country_code_fuzzy(country_name)
            isos.append(iso)

        datasets = []
        for name, dataset_info in self._configuration["datasets"].items():
            dataset_title = (
                f"Social Indicators of Latin America and the Caribbean: {name}"
            )
            dataset = Dataset(
                {
                    "name": slugify(dataset_title),
                    "title": dataset_title,
                }
            )

            dataset.set_time_period(start_date, end_date)
            dataset.add_tags(dataset_info["tags"])
            dataset.add_country_locations(isos)

            resource_names = dataset_info["resources"]
            resource_list = ["- " + r for r in resource_names]
            dataset["notes"] = (
                self._configuration["notes"]
                + "  \n  \nThis dataset includes the following indicators:  \n"
                + "  \n".join(resource_list)
            )

            # Add resources
            resources_info = [
                r for r in metadata["resources"] if r["name"] in resource_names
            ]
            if len(resources_info) < len(resource_names):
                logger.error(f"{name}: not all resources listed in config were found")
            for resource_info in resources_info:
                resource = {
                    "name": resource_info["name"],
                    "description": resource_info["description"],
                    "url": resource_info["url"],
                    "format": "csv",
                }
                dataset.add_update_resource(resource)
            datasets.append(dataset)

        return datasets
