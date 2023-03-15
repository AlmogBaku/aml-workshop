#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from __future__ import annotations

import pandas as pd
import pendulum

from airflow.decorators import dag, task


# [START dag_decorator_usage]
@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example", "aml-workshop"],
)
def simple_xgboost():
    """
    Simple DAG
    """

    @task
    def load_train_data():
        """
        data from https://www.kaggle.com/c/home-data-for-ml-course/data
        :return:
        """
        return pd.read_csv("/opt/airflow/dags/home-data-for-ml-course/train.csv").to_json()

    @task
    def clean_data(data):
        data = pd.read_json(data)
        return data.dropna().to_json()

    @task
    def ret_hey():
        return "hey"

    @task
    def ret_hoy():
        return "hoy"

    @task
    def say(data, a, b):
        print(pd.read_json(data).head())
        print(a, b)

    @task
    def train_model(data):
        data = pd.read_json(data)
        from xgboost import XGBRegressor

        model = XGBRegressor(n_estimators=1000, learning_rate=0.05, n_jobs=4)
        model.fit(data.drop('SalePrice', axis=1), data['SalePrice'])

        model.save_model("/opt/airflow/dags/xgboost.model.ubj")

    data = clean_data(load_train_data())
    say(data, ret_hey(), ret_hoy())
    train_model(data)

    # load_train_data >> clean_data >> train_model >> save_model


dag = simple_xgboost()
# [END dag_decorator_usage]
