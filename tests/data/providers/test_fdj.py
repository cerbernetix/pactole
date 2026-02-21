"""Unit tests for FDJ providers."""

from __future__ import annotations

from unittest.mock import patch

from pactole.data.providers.fdj import FDJResolver


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
