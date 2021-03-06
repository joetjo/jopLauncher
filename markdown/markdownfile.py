# Copyright 2021 joetjo https://github.com/joetjo/MarkdownHelper
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
import re


class MhMarkdownFile:

    # name : String
    # path : Path from PathLib
    def __init__(self, name, path):
        # String
        self.name = name
        # WindowsPath ( from pathLib )
        self.path = path
        self.tags = []
        self.tagsComment = dict()
        self.loadTags()
        self.matchTag = None

    def loadTags(self):
        with open(self.path, 'r', encoding='utf8') as reader:
            for line in reader:
                # Search for tag beginning of line for extended comment
                if line.startswith("#"):
                    lineTags = re.findall(r"^#[\w|/_-]+", line)
                    if len(lineTags) > 0:
                        lineTag = lineTags[0]
                        comment = line[len(lineTag):len(line) - 1]
                        if len(comment) > 0:
                            try:
                                comments = self.tagsComment[lineTag]
                            except KeyError:
                                comments = []
                                self.tagsComment[lineTag] = comments
                            comments.append(comment)
                # Extract all tags
                rawTags = re.findall(r"#[\w|/_-]+[\s\S]", line)
                for tag in rawTags:
                    self.tags.append(tag.rstrip())

    def getTagComment(self, tag):
        try:
            return self.tagsComment["#{}".format(tag)]
        except KeyError:
            return None

    # expr : re regexp
    def pathMatch(self, path):
        return str(self.path.resolve()).find(path) != -1

    # Search tag like #XXXXX ( with tag = '#XXXXX' )
    def hasExactTag(self, tag):
        result = tag in self.tags
        if result:
            self.matchTag = tag

    # Search tag like #XXXXX....  ( with prefix = '#XXXXX' )
    def hasTagStartingBy(self, prefix):
        token = "#{}".format(prefix)
        for tag in self.tags:
            if tag.startswith(token):
                self.matchTag = tag
                return True
        return False

    def getTagStartingBy(self, prefix):
        result = []
        token = "#{}".format(prefix)
        for tag in self.tags:
            if tag.startswith(token):
                result.append(tag)
        return result
