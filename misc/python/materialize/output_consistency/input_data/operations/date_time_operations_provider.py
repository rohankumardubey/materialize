# Copyright Materialize, Inc. and contributors. All rights reserved.
#
# Use of this software is governed by the Business Source License
# included in the LICENSE file at the root of this repository.
#
# As of the Change Date specified in that file, in accordance with
# the Business Source License, use of this software will be governed
# by the Apache License, Version 2.0.

from materialize.output_consistency.expression.expression_characteristics import (
    ExpressionCharacteristics,
)
from materialize.output_consistency.input_data.params.date_time_operation_param import (
    DateTimeOperationParam,
    TimeIntervalOperationParam,
)
from materialize.output_consistency.input_data.params.enum_constant_operation_params import (
    DATE_TIME_COMPONENT_PARAM,
    ISO8601_TIMESTAMP_PARAM,
    PRECISION_PARAM,
    TIME_COMPONENT_PARAM,
    TIME_ZONE_PARAM,
    TYPE_FORMAT_PARAM,
)
from materialize.output_consistency.input_data.params.number_operation_param import (
    NumericOperationParam,
)
from materialize.output_consistency.input_data.return_specs.date_time_return_spec import (
    DateTimeReturnTypeSpec,
)
from materialize.output_consistency.input_data.return_specs.number_return_spec import (
    NumericReturnTypeSpec,
)
from materialize.output_consistency.input_data.return_specs.string_return_spec import (
    StringReturnTypeSpec,
)
from materialize.output_consistency.input_data.types.date_time_types_provider import (
    INTERVAL_TYPE_IDENTIFIER,
    TIMESTAMP_TYPE_IDENTIFIER,
    TIMESTAMPTZ_TYPE_IDENTIFIER,
)
from materialize.output_consistency.operation.operation import (
    DbFunction,
    DbOperation,
    DbOperationOrFunction,
    OperationRelevance,
)

DATE_TIME_OPERATION_TYPES: list[DbOperationOrFunction] = []

DATE_TIME_OPERATION_TYPES.append(
    DbFunction(
        "age",
        [
            DateTimeOperationParam(support_time=False),
            DateTimeOperationParam(support_time=False),
        ],
        DateTimeReturnTypeSpec(INTERVAL_TYPE_IDENTIFIER),
        relevance=OperationRelevance.LOW,
    )
)

DATE_TIME_OPERATION_TYPES.append(
    DbFunction(
        "date_bin",
        [
            TimeIntervalOperationParam(
                incompatibilities={
                    ExpressionCharacteristics.INTERVAL_WITH_MONTHS,
                    ExpressionCharacteristics.MAX_VALUE,
                }
            ),
            DateTimeOperationParam(support_time=False),
            DateTimeOperationParam(support_time=False),
        ],
        DateTimeReturnTypeSpec(TIMESTAMP_TYPE_IDENTIFIER),
        relevance=OperationRelevance.LOW,
        # TODO gets stuck, may get better when appropriate input can be ensured
        is_enabled=False,
    )
)

DATE_TIME_OPERATION_TYPES.append(
    DbFunction(
        "date_trunc",
        [DATE_TIME_COMPONENT_PARAM, DateTimeOperationParam()],
        DateTimeReturnTypeSpec(TIMESTAMP_TYPE_IDENTIFIER),
        comment="for date types other than interval",
    )
)

DATE_TIME_OPERATION_TYPES.append(
    DbFunction(
        "date_trunc",
        [DATE_TIME_COMPONENT_PARAM, TimeIntervalOperationParam()],
        DateTimeReturnTypeSpec(INTERVAL_TYPE_IDENTIFIER),
        comment="for interval type",
    )
)

DATE_TIME_OPERATION_TYPES.append(
    DbOperation(
        "EXTRACT($ FROM $)",
        [DATE_TIME_COMPONENT_PARAM, DateTimeOperationParam(support_time=False)],
        NumericReturnTypeSpec(),
        comment="for date types",
    )
)

DATE_TIME_OPERATION_TYPES.append(
    DbOperation(
        "EXTRACT($ FROM $)",
        [TIME_COMPONENT_PARAM, DateTimeOperationParam(support_date=False)],
        NumericReturnTypeSpec(),
        comment="for time types",
    )
)

DATE_TIME_OPERATION_TYPES.append(
    DbOperation(
        "EXTRACT($ FROM $)",
        [DATE_TIME_COMPONENT_PARAM, TimeIntervalOperationParam()],
        NumericReturnTypeSpec(),
        comment="for interval type",
    )
)

DATE_TIME_OPERATION_TYPES.append(
    DbFunction(
        "date_part",
        [DATE_TIME_COMPONENT_PARAM, DateTimeOperationParam()],
        NumericReturnTypeSpec(),
        comment="for date types other than interval",
    )
)

DATE_TIME_OPERATION_TYPES.append(
    DbFunction(
        "date_part",
        [DATE_TIME_COMPONENT_PARAM, TimeIntervalOperationParam()],
        NumericReturnTypeSpec(),
        comment="for interval type",
    )
)

DATE_TIME_OPERATION_TYPES.append(
    DbOperation(
        "$ AT TIME ZONE $::TEXT",
        [DateTimeOperationParam(support_time=False), TIME_ZONE_PARAM],
        DateTimeReturnTypeSpec(TIMESTAMPTZ_TYPE_IDENTIFIER),
    )
)

DATE_TIME_OPERATION_TYPES.append(
    DbFunction(
        "timezone",
        [TIME_ZONE_PARAM, DateTimeOperationParam(support_time=False)],
        DateTimeReturnTypeSpec(TIMESTAMPTZ_TYPE_IDENTIFIER),
    )
)

DATE_TIME_OPERATION_TYPES.append(
    DbFunction(
        "to_timestamp",
        [NumericOperationParam()],
        DateTimeReturnTypeSpec(TIMESTAMPTZ_TYPE_IDENTIFIER),
    )
)

DATE_TIME_OPERATION_TYPES.append(
    DbFunction(
        "to_char",
        [DateTimeOperationParam(support_time=False), TYPE_FORMAT_PARAM],
        StringReturnTypeSpec(),
    )
)

DATE_TIME_OPERATION_TYPES.append(
    DbFunction(
        "try_parse_monotonic_iso8601_timestamp",
        [ISO8601_TIMESTAMP_PARAM],
        DateTimeReturnTypeSpec(TIMESTAMP_TYPE_IDENTIFIER),
        is_pg_compatible=False,
    )
)

DATE_TIME_OPERATION_TYPES.append(
    DbFunction(
        "justify_days",
        [
            DateTimeOperationParam(
                support_date=False,
                support_time=True,
                support_timestamp=False,
                support_timestamp_tz=False,
            )
        ],
        DateTimeReturnTypeSpec(INTERVAL_TYPE_IDENTIFIER),
        comment="for time type",
    )
)

DATE_TIME_OPERATION_TYPES.append(
    DbFunction(
        "justify_days",
        [TimeIntervalOperationParam()],
        DateTimeReturnTypeSpec(INTERVAL_TYPE_IDENTIFIER),
        comment="for interval type",
    )
)

DATE_TIME_OPERATION_TYPES.append(
    DbFunction(
        "justify_hours",
        [
            DateTimeOperationParam(
                support_date=False,
                support_time=True,
                support_timestamp=False,
                support_timestamp_tz=False,
            )
        ],
        DateTimeReturnTypeSpec(INTERVAL_TYPE_IDENTIFIER),
        comment="for time type",
    )
)

DATE_TIME_OPERATION_TYPES.append(
    DbFunction(
        "justify_hours",
        [TimeIntervalOperationParam()],
        DateTimeReturnTypeSpec(INTERVAL_TYPE_IDENTIFIER),
        comment="for interval type",
    )
)

DATE_TIME_OPERATION_TYPES.append(
    DbFunction(
        "justify_interval",
        [
            DateTimeOperationParam(
                support_date=False,
                support_time=True,
                support_timestamp=False,
                support_timestamp_tz=False,
            )
        ],
        DateTimeReturnTypeSpec(INTERVAL_TYPE_IDENTIFIER),
        comment="for time type",
    )
)

DATE_TIME_OPERATION_TYPES.append(
    DbFunction(
        "justify_interval",
        [TimeIntervalOperationParam()],
        DateTimeReturnTypeSpec(INTERVAL_TYPE_IDENTIFIER),
        comment="for interval type",
    )
)

DATE_TIME_OPERATION_TYPES.append(
    DbOperation(
        "$::TIMESTAMP($)",
        [DateTimeOperationParam(), PRECISION_PARAM],
        DateTimeReturnTypeSpec(TIMESTAMP_TYPE_IDENTIFIER),
        comment="for TIMESTAMP type",
    )
)

DATE_TIME_OPERATION_TYPES.append(
    DbOperation(
        "$::TIMESTAMPTZ($)",
        [DateTimeOperationParam(), PRECISION_PARAM],
        DateTimeReturnTypeSpec(TIMESTAMPTZ_TYPE_IDENTIFIER),
        comment="for TIMESTAMPTZ type",
    )
)

DATE_TIME_OPERATION_TYPES.append(
    DbOperation(
        "$ + $",
        [DateTimeOperationParam(), TimeIntervalOperationParam()],
        DateTimeReturnTypeSpec(TIMESTAMPTZ_TYPE_IDENTIFIER),
        comment="with interval type as second operator",
    )
)
DATE_TIME_OPERATION_TYPES.append(
    DbOperation(
        "$ - $",
        [DateTimeOperationParam(), TimeIntervalOperationParam()],
        DateTimeReturnTypeSpec(TIMESTAMPTZ_TYPE_IDENTIFIER),
        comment="with interval type as second operator",
    )
)

DATE_TIME_OPERATION_TYPES.append(
    DbOperation(
        "$ + $",
        [DateTimeOperationParam(), DateTimeOperationParam()],
        DateTimeReturnTypeSpec(TIMESTAMPTZ_TYPE_IDENTIFIER),
        comment="with date-time type as second operator",
    )
)
DATE_TIME_OPERATION_TYPES.append(
    DbOperation(
        "$ - $",
        [DateTimeOperationParam(), DateTimeOperationParam()],
        DateTimeReturnTypeSpec(TIMESTAMPTZ_TYPE_IDENTIFIER),
        comment="with date-time type as second operator",
    )
)
