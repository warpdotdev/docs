from rich import print
from typing import Optional

from pydantic import BaseModel
from typing import List


class Copyrights(BaseModel):
    statements: List[str]


class License_Expression(BaseModel):
    license_expression: str

    def as_string(self):
        return str(self.license_expression).upper()


class Conclusion(BaseModel):
    code_type: str
    copyright: str
    copyrights: List[Copyrights]
    feature: str
    fileId: int
    homepage_url: str
    license_expression: List[License_Expression]
    name: str
    notes: str
    owner: str
    path: str
    purpose: str
    review_status: str
    version: str
    download_url: Optional[str]
    is_deployed: Optional[bool]
    is_modified: Optional[bool]
    license_url: Optional[str]
    notice_url: Optional[str]
    programming_language: Optional[bool]
    purl: Optional[bool]


class Model(BaseModel):
    conclusions: List[Conclusion]
    workbench_version: str
    workbench_notice: str

    def as_markdown(self):
        markdown: List[str] = [
            "## ScanCode licenses",
            "\n\n",
            "|Name|License|Copyright|",
            "\n",
            "|---|---|---:|",
            "\n",
        ]

        already_added_conclusions_list: List[str] = []
        markdown_conclusion: List[str] = []

        for conclusion in self.conclusions:
            license_expression: str = ""
            if license_list := conclusion.license_expression:
                if first_license := license_list[0]:
                    license_expression = first_license.as_string()

            name: str = conclusion.name
            if name not in already_added_conclusions_list:
                already_added_conclusions_list.append(name)
                markdown_conclusion.append(
                    f"| {name} | {license_expression} | {conclusion.copyright} |" f"\n"
                )
        markdown.extend(sorted(markdown_conclusion))
        return markdown


def run(input_filename: str) -> None:
    model = Model.parse_file(input_filename)
    return model.as_markdown()
