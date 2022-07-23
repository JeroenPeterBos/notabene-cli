"""Tests of the template commands."""
import shutil
from pathlib import Path

import pytest

from notabene.base import Project
from notabene.cli import cli
from tests.testing_utils import CliRunner

# pylint: disable=unused-argument


@pytest.fixture
def pf_data_path(request):
    """Fixture that resolves the path to the test data directory."""
    test_file = Path(request.module.__file__)
    return test_file.parent / "data" / test_file.stem


@pytest.fixture
def pf_empty(pf_data_path: Path, tmp_path: Path):
    """Fixture project with only a 'pyproject.toml' file."""
    shutil.copy(
        pf_data_path / "pyproject.toml",
        tmp_path,
    )
    return tmp_path


@pytest.fixture
def pf_template(pf_data_path: Path, pf_empty: Path):
    """Fixture project with one registered template."""
    template_path = pf_empty / ".notabene" / "templates"
    template_path.mkdir(parents=True, exist_ok=True)

    shutil.copy(
        pf_data_path / "templates" / "exploratory_data_analysis.ipynb",
        template_path,
    )
    return pf_empty


@pytest.fixture
def pf_notebook(pf_data_path: Path, pf_empty: Path):
    """Fixture project with one notebook."""
    notebook_path = pf_empty / "notebooks"
    notebook_path.mkdir(parents=True, exist_ok=True)

    shutil.copy(
        pf_data_path / "notebooks" / "test_eda.ipynb",
        notebook_path,
    )
    return pf_empty


@pytest.fixture
def pf_template_notebook(pf_template: Path, pf_notebook: Path):
    """Fixture project with one notebook and one template."""
    return pf_template


def test_fixtures(
    pf_empty: Path,
    pf_template: Path,
    pf_notebook: Path,
    pf_template_notebook: Path,
):
    """Test that the fixtures contain the appropriate notebooks and templates."""
    all_fixtures = {pf_empty, pf_template, pf_notebook, pf_template_notebook}
    with_template = {pf_template, pf_template_notebook}
    with_notebook = {pf_notebook, pf_template_notebook}

    for fixture in all_fixtures:
        assert (fixture / "pyproject.toml").exists()

        template_path = fixture / ".notabene/templates/exploratory_data_analysis.ipynb"
        if fixture in with_template:
            assert template_path.exists()
        else:
            assert not template_path.exists()

        notebook_path = fixture / "notebooks/test_eda.ipynb"
        if fixture in with_notebook:
            assert notebook_path.exists()
        else:
            assert not notebook_path.exists()


class TestList:
    """Tests related to the 'list' command."""

    def test_list_basic(self, pf_template: Path):
        """Test listing templates."""
        with CliRunner().enter_fixture(path=pf_template) as runner:
            result = runner.invoke(cli, ["template", "list"])

            assert result.exit_code == 0
            assert "The available templates are" in result.output
            assert "exploratory_data_analysis" in result.output

    def test_list_empty_project(self, pf_empty: Path):
        """Test listing templates with no templates."""
        with CliRunner().enter_fixture(path=pf_empty) as runner:
            result = runner.invoke(cli, ["template", "list"])

            assert result.exit_code == 0
            assert "You don't have any templates yet." in result.output


class TestCreate:
    """Tests related to the 'create' command."""

    @pytest.mark.parametrize(
        "name",
        [
            "eda",
            "IncorrectName\ngood_name",
            "failing_\n_correct",
            "exploratory_data_analysis\neda",
        ],
    )
    def test_create_basic(self, pf_template_notebook: Path, name: str):
        """Test create a new template."""
        with CliRunner().enter_fixture(path=pf_template_notebook) as runner:
            initial_no_templates = len(Project().get_templates())
            result = runner.invoke(
                cli, ["template", "create", "notebooks/test_eda.ipynb"], input=name
            )

            assert result.exit_code == 0
            templates = Project().get_templates()
            assert len(templates) == initial_no_templates + 1
            assert name.split("\n")[-1].split(".")[0] in [t.stem for t in templates]

    def test_name_option(self, pf_notebook: Path):
        """Test create a new template."""
        with CliRunner().enter_fixture(path=pf_notebook) as runner:
            result = runner.invoke(
                cli,
                [
                    "template",
                    "create",
                    "--name",
                    "exploratory_data_analysis",
                    "notebooks/test_eda.ipynb",
                ],
            )

            assert result.exit_code == 0
