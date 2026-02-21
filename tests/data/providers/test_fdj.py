"""Unit tests for FDJ providers."""

from __future__ import annotations

import datetime
from unittest.mock import patch

from pactole.combinations import LotteryCombination
from pactole.data.providers.fdj import FDJParser, FDJResolver


class TestFDJResolver:
    """Tests for the FDJResolver class."""

    def test_get_archives_page_url_uses_default_template(self) -> None:
        """Test building archive URLs using the default template."""

        assert (
            FDJResolver.get_archives_page_url("euromillions-my-million")
            == "https://www.fdj.fr/jeux-de-tirage/euromillions-my-million/historique"
        )

    def test_get_archives_page_url_uses_env_template(self) -> None:
        """Test building archive URLs using the env template override."""

        template = "https://local.test/archives/{name}/history"
        with patch.dict("os.environ", {"FDJ_ARCHIVES_PAGE_URL": template}):
            assert (
                FDJResolver.get_archives_page_url("eurodreams")
                == "https://local.test/archives/eurodreams/history"
            )

    def test_get_archives_page_url_requires_placeholder(self) -> None:
        """Test missing template placeholder raises a ValueError."""

        with patch.dict("os.environ", {"FDJ_ARCHIVES_PAGE_URL": "https://local.test/archives"}):
            try:
                FDJResolver.get_archives_page_url("eurodreams")
            except ValueError as exc:
                assert "{name}" in str(exc)
            else:
                raise AssertionError("Expected ValueError when template lacks '{name}'.")

    def test_load_cache_parses_download_links(self) -> None:
        """Test that the resolver extracts download links from the archive page."""

        html = (
            "<html><body>"
            '<a download="archive_202401" href="https://local.test/a.csv"></a>'
            '<a download="archive_202402" href="https://local.test/b.csv"></a>'
            "</body></html>"
        )

        def fake_fetch_content(url: str) -> str:
            assert url == "https://local.test/archives"
            return html

        with patch("pactole.data.providers.fdj.fetch_content", fake_fetch_content):
            resolver = FDJResolver("https://local.test/archives")

            assert resolver.load() == {
                "archive_202401": "https://local.test/a.csv",
                "archive_202402": "https://local.test/b.csv",
            }

    def test_init_accepts_lottery_name(self) -> None:
        """Test initializing the resolver with a lottery name uses the template."""

        html = "<html><body></body></html>"

        def fake_fetch_content(url: str) -> str:
            assert url == "https://www.fdj.fr/jeux-de-tirage/euromillions-my-million/historique"
            return html

        with patch("pactole.data.providers.fdj.fetch_content", fake_fetch_content):
            resolver = FDJResolver("euromillions-my-million")

            assert resolver.load() == {}


class TestFDJParser:
    """Tests for the FDJParser class."""

    def test_format_date_supports_multiple_formats(self) -> None:
        """Test date normalization for supported date formats."""

        def combination_factory(**_: list[int]) -> LotteryCombination:
            return LotteryCombination(winning_ranks={(5, 0): 1})

        parser = FDJParser(combination_factory=combination_factory)

        base_data = {
            "date_de_forclusion": "2024-02-15",
            "boule_1": "1",
            "boule_2": "2",
            "boule_3": "3",
            "boule_4": "4",
            "boule_5": "5",
        }

        record_iso = parser({"date_de_tirage": "2024-02-01", **base_data})
        record_rfc = parser({"date_de_tirage": "20240201", **base_data})
        record_fr = parser({"date_de_tirage": "01/02/24", **base_data})

        assert record_iso.draw_date == datetime.date(2024, 2, 1)
        assert record_rfc.draw_date == datetime.date(2024, 2, 1)
        assert record_fr.draw_date == datetime.date(2024, 2, 1)

    def test_call_builds_draw_record(self) -> None:
        """Test parsing builds a draw record with numbers and winning ranks."""

        captured: dict[str, list[int]] = {}

        def combination_factory(**numbers: list[int]) -> LotteryCombination:
            captured.update(numbers)
            return LotteryCombination(winning_ranks={(5, 1): 1, (5, 0): 2})

        parser = FDJParser(combination_factory=combination_factory)
        data = {
            "date_de_tirage": "01/02/24",
            "date_de_forclusion": "20240215",
            "boule_1": "1",
            "boule_2": "2",
            "boule": "3",
            "etoile_1": "9",
            "etoile_2": "10",
            "numero_dream": "7",
            "ignored_field": "noop",
            "nombre_de_gagnant_au_rang1_en_europe": "2",
            "rapport_du_rang1": "1000000.0",
            "nombre_de_gagnant_au_rang2": "4",
            "rapport_du_rang2": "50000.0",
        }

        record = parser(data)

        assert record.draw_date == datetime.date(2024, 2, 1)
        assert record.deadline_date == datetime.date(2024, 2, 15)
        assert captured == {
            "numbers": [1, 2, 3],
            "stars": [9, 10],
            "dream": [7],
        }
        assert record.numbers == captured
        assert [(rank.rank, rank.winners, rank.gain) for rank in record.winning_ranks] == [
            (1, 2, 1000000.0),
            (2, 4, 50000.0),
        ]

    def test_call_keeps_first_winners_and_gains(self) -> None:
        """Test duplicate winner and gain keys keep the first values."""

        captured: dict[str, list[int]] = {}

        def combination_factory(**numbers: list[int]) -> LotteryCombination:
            captured.update(numbers)
            return LotteryCombination(winning_ranks={(5, 0): 1, (4, 0): 2})

        parser = FDJParser(combination_factory=combination_factory)
        data = {
            "date_de_tirage": "2024-02-01",
            "date_de_forclusion": "2024-02-15",
            "bonus_1": "8",
            "nombre_de_gagnant_au_rang1_en_europe": "2",
            "nombre_de_gagnant_au_rang1": "99",
            "rapport_du_rang1": "100.0",
            "rapport_du_rang1_en_europe": "999.0",
        }

        record = parser(data)

        assert record.numbers == {"bonus": [8]}
        assert captured == {"bonus": [8]}
        assert [(rank.rank, rank.winners, rank.gain) for rank in record.winning_ranks] == [
            (1, 2, 100.0),
            (2, 0, 0.0),
        ]

    def test_call_handles_combinations_without_winning_ranks(self) -> None:
        """Test parsing returns no winning ranks when the combination has none."""

        def combination_factory(**_: list[int]) -> LotteryCombination:
            return LotteryCombination()

        parser = FDJParser(combination_factory=combination_factory)
        data = {
            "date_de_tirage": "2024-02-01",
            "date_de_forclusion": "2024-02-15",
            "boule_1": "1",
            "boule_2": "2",
        }

        record = parser(data)

        assert not record.winning_ranks
