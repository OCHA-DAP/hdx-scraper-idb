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

        isos = []
        for location in metadata["spatial_coverage"]:
            country_name = location["label"]["en"]
            iso, _ = Country.get_iso3_country_code_fuzzy(country_name)
            isos.append(iso)

        datasets = []
        for name, dataset_info in self._configuration["datasets"].items():
            dataset_title = f"Latin America and the Caribbean: {name}"
            dataset_name = slugify(f"IDB-{name}")
            dataset = Dataset(
                {
                    "name": dataset_name,
                    "title": dataset_title,
                }
            )

            dataset.add_tags(dataset_info["tags"])
            dataset.add_country_locations(isos)

            resource_names = dataset_info["resources"]
            resource_list = ["- " + r for r in resource_names]
            dataset["notes"] = (
                self._configuration["notes"]
                + "  \n  \nThis dataset includes the following indicators:  \n"
                + "  \n".join(resource_list)
                + "  \n  \nFor links to individual indicator metadata and methodologies, see resource descriptions."
            )

            # Add resources
            resources_info = [
                r for r in metadata["resources"] if r["name"] in resource_names
            ]
            if len(resources_info) < len(resource_names):
                logger.error(f"{name}: not all resources listed in config were found")
            if len(resources_info) > len(resource_names):
                for i, r in enumerate(resources_info):
                    r["name"] = f"{r['name']} ({i + 1})"
                    resources_info[i] = r
            if len(resources_info) == len(resource_names):
                resources_info_names = [r["name"] for r in resources_info]
                resources_order = [
                    resources_info_names.index(name) for name in resource_names
                ]
                resources_info = [resources_info[index] for index in resources_order]

            resource_years = set()
            for resource_info in resources_info:
                download_url = resource_info["url"]
                resource = {
                    "name": resource_info["name"],
                    "description": resource_info["description"],
                    "url": download_url,
                    "format": "csv",
                }
                dataset.add_update_resource(resource)
                headers, rows = self._retriever.get_tabular_rows(
                    download_url, format="csv"
                )
                year_i = headers.index("year")
                for row in rows:
                    resource_years.add(row[year_i])
            dataset.set_time_period_year_range(min(resource_years), max(resource_years))
            datasets.append(dataset)

        return datasets
