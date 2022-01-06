from typing import Optional

from pydantic import BaseModel
from typing import List


class Crate(BaseModel):
    name: str
    version: str
    license: Optional[str]
    authors: Optional[str]
    repository: Optional[str]
    description: Optional[str]
    license_file: Optional[str]


def strip_github(
    repo_url: str,
) -> str:
    github_url: str = "github.com/"
    try:
        github_string_index: int = repo_url.index(github_url)
    except TypeError:
        return ""
    except AttributeError:
        return ""
    except ValueError:
        return ""

    return repo_url[github_string_index + len(github_url) :]


class Model(BaseModel):
    model: List[Crate]

    def as_markdown(self) -> List[str]:
        markdown: List[str] = [
            "## Cargo based licenses",
            "\n\n",
            "Repositories are by default GitHub if not otherwise specified",
            "\n\n",
            "| Name | License | Repository |",
            "\n",
            "|---|---|---:|",
            "\n",
        ]
        crate_markdown: List[str] = []
        for crate in self.model:
            if crate.license:
                crate_markdown.append(
                    f"| {crate.name} | {crate.license} | {strip_github(crate.repository)} |"
                    f"\n"
                )
        markdown.extend(sorted(crate_markdown))
        markdown.append("\n")
        return markdown
