import shutil
from pathlib import Path

import pytest
from click.testing import CliRunner
from notabene.cli import cli


@pytest.fixture
def pf_data_path(request):
    test_file = Path(request.module.__file__)
    return test_file.parent / "data" / test_file.stem


@pytest.fixture
def pf_empty(pf_data_path: Path, tmp_path: Path):
    shutil.copy(
        pf_data_path / "pyproject.toml",
        tmp_path,
    )
    return tmp_path


@pytest.fixture
def pf_template(pf_data_path: Path, pf_empty: Path):
    template_path = pf_empty / ".notabene" / "templates"
    template_path.mkdir(parents=True, exist_ok=True)

    shutil.copy(
        pf_data_path / "templates" / "exploratory_data_analysis.ipynb",
        template_path,
    )
    return pf_empty


@pytest.fixture
def pf_notebook(pf_data_path: Path, pf_empty: Path):
    notebook_path = pf_empty / "notebooks"
    notebook_path.mkdir(parents=True, exist_ok=True)

    shutil.copy(
        pf_data_path / "notebooks" / "test_eda.ipynb",
        notebook_path,
    )
    return pf_empty


@pytest.fixture
def pf_template_notebook(pf_template: Path, pf_notebook: Path):
    return pf_template


def test_fixtures(
    pf_empty: Path,
    pf_template: Path,
    pf_notebook: Path,
    pf_template_notebook: Path,
):
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


def test_list_empty(pf_empty: Path):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=pf_empty):
        result = runner.invoke(cli, ["template", "list"])
        assert result.exit_code == 0
        assert "You don't have any templates yet." in result.output


def test_list(pf_template: Path):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=pf_template):
        result = runner.invoke(cli, ["template", "list"])
        assert result.exit_code == 0
        assert "The available templates are" in result.output
        assert "exploratory_data_analysis" in result.output
