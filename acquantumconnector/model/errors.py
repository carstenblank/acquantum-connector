#  Copyright (c) 2019.  Carsten Blank
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


class AcQuantumRequestError(Exception):
    def __init__(self, message, status_code=None):
        # type: (str, int) -> None
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return 'AcRequestError: \'{}\''.format(self.message)

    def __repr__(self):
        return 'AcRequestError: \'{}\''.format(self.message)


class AcQuantumRequestForbiddenError(AcQuantumRequestError):
    def __init__(self, message='403 Forbidden'):
        # type: (str) -> None
        self.message = message

    def __str__(self):
        return '403 - AcRequestForbiddenError: \'{}\''.format(self.message)

    def __repr__(self):
        return '403 - AcRequestForbiddenError: \'{}\''.format(self.message)
