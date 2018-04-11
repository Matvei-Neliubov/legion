#
#    Copyright 2017 EPAM Systems
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
"""
Models (base, interfaces and proxies)
"""
import functools
import logging

from interface import implements
from legion_core.model.types import build_df
from legion_core.model.model import IMLModel
from legion_pyserve.builder import build

LOGGER = logging.getLogger('deploy')


class ScipyModel(implements(IMLModel)):
    """
    A simple model using Pandas DF for internal representation.
    Useful for Sklearn/Scipy based model export
    """

    def __init__(self, apply_func, prepare_func, column_types, version='Unknown', use_df=True):
        """
        Build simple SciPy model

        :param apply_func: an apply function DF->DF
        :type apply_func: func(x) -> y
        :param prepare_func: a function to prepare input DF->DF
        :type prepare_func: func(x) -> y
        :param column_types: dict of column name => type or None
        :type column_types: dict[str, :py:class:`legion.types.ColumnInformation`] or None
        :param version: version of model
        :param use_df: use pandas DF for prepare and apply function
        :type use_df: bool
        :type version: str
        """
        assert apply_func is not None
        assert prepare_func is not None

        self.apply_func = apply_func
        self.column_types = column_types
        self.prepare_func = prepare_func
        self.version = version
        self.use_df = use_df

    def apply(self, input_vector):
        """
        Calculate result of model execution

        :param input_vector: input data
        :type input_vector: dict[str, union[str, Image]]
        :return: dict -- output data
        """
        LOGGER.info('Input vector: %r' % input_vector)
        data_frame = build_df(self.column_types, input_vector, not self.use_df)

        LOGGER.info('Running prepare with DataFrame: %r' % data_frame)
        data_frame = self.prepare_func(data_frame)

        LOGGER.info('Applying function with DataFrame: %s' % str(data_frame))
        response = self.apply_func(data_frame)
        LOGGER.info('Returning response: %s' % str(response))

        return response

    @property
    def version_string(self):
        """
        Get model version

        :return: str -- version
        """
        return self.version

    @property
    def description(self):
        """
        Get model description

        :return: dict[str, any] with model description
        """
        data = {
            'version': self.version,
            'use_df': self.use_df
        }

        if self.column_types:
            data['input_params'] = {k: v.description_for_api for (k, v) in self.column_types.items()}
        else:
            data['input_params'] = False

        return data

    @staticmethod
    def get_builder():
        return functools.partial(build, ScipyModel)
