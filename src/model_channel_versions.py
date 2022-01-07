import re
from datetime import datetime
from typing import Dict
from typing import List

from pydantic import BaseModel

CHANNEL_VERSIONS_FILE_NAME: str = "channel_versions.json"
OUTPUT_DATE_TIME_FORMAT: str = "%Y-%m-%d"
STABLE: str = "stable"
GITHUB_ISSUE_LINK: str = "https://github.com/warpdotdev/warp/issues/"
RE_GITHUB_ISSUE: str = r"#(\d\d\d)"
RE_GITHUB_ISSUE_PATTERN = re.compile(RE_GITHUB_ISSUE)


class Section(BaseModel):
    title: str
    items: List[str]

    def as_discord_message(self):
        output: str = f"** ***{self.title}*\n"
        for item in self.items:
            output = output + f"- {item}\n"
        return output

    def as_message(self):
        output: str = f"\n**{self.title}**\n\n"
        item: str

        for item in self.items:
            cleaned_item = item
            search_object = re.search(RE_GITHUB_ISSUE_PATTERN, item)
            if search_object:
                cleaned_item = re.sub(
                    RE_GITHUB_ISSUE_PATTERN,
                    r"[\1](https://github.com/warpdotdev/warp/issues/\1)",
                    item,
                )
            output = output + f"- {cleaned_item}\n"

        return output


class Changelog(BaseModel):
    date: datetime
    sections: List[Section]

    def get_date(self):
        return f"{self.date.strftime(OUTPUT_DATE_TIME_FORMAT)}"


# noinspection PyPep8Naming
class Model(BaseModel):
    dev: Dict[str, str]
    beta: Dict[str, str]
    stable: Dict[str, str]
    changelogs: Dict[str, Dict[str, Changelog]]

    def get_changelogs(
        self,
        channel_name: str,
    ) -> Dict[str, Changelog]:
        channel_changelogs: Dict[str, Changelog] = self.changelogs.get(
            channel_name,
            {},
        )
        if not channel_changelogs:
            raise Exception(f"No changelogs exist for {channel_name}.")
        return channel_changelogs

    def add_changelog(
        self,
        channel_name: str,
        channel_version: str,
        changelog: Changelog,
    ) -> None:
        if not channel_name:
            raise Exception("empty channel name")
        if not channel_version:
            raise Exception("empty channel version")
        if not changelog:
            raise Exception("empty changelog")

        self.changelogs.update(
            {
                channel_name: {channel_version: changelog}
                | self.changelogs[
                    channel_name
                ]  # | pipe operator merges two dictionaries
            }
        )

    def as_markdown(self):
        def strip_key(changelog_key: str) -> str:
            last_period = changelog_key.rindex(".")
            return changelog_key[:last_period]

        stable_changelogs = self.get_changelogs(STABLE)

        changelog: Changelog

        markdown: List[str] = []
        already_added_changelog_key_list: List[str] = []
        for key in reversed(stable_changelogs):
            key_md = strip_key(key)
            if key_md not in already_added_changelog_key_list:
                changelog = stable_changelogs.get(key, {})
                if changelog:
                    already_added_changelog_key_list.append(key_md)
                    markdown.append(f"### {changelog.get_date()} ({key_md})\n")
                    markdown.extend(
                        [
                            section.as_message()
                            for section in changelog.sections
                            if section.title != "Coming soon"
                        ]
                    )
                    markdown.append("\n")

        return markdown
