# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

from llama_stack.apis.scoring_functions import *  # noqa: F401, F403
from llama_stack.apis.scoring import *  # noqa: F401, F403
from llama_stack.apis.common.type_system import NumberType

regex_parser_base = ScoringFn(
    identifier="basic::regex_parser_base",
    description="Regex Parser Base Scoring Function. Specify parsing_regexes to extract the answer from the response.",
    return_type=NumberType(),
    provider_id="basic",
    provider_resource_id="regex-parser-base",
    params=RegexParserScoringFnParams(
        parsing_regexes=None,
    ),
)
