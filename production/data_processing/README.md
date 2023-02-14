# Data_processing
![version](https://img.shields.io/badge/version-v1.0-white)
![python](https://img.shields.io/badge/python-v3.8-blue)
![make](https://img.shields.io/badge/make-v4.2.1-blue)
![aws](https://img.shields.io/badge/platform-aws-orange)



## Objective

Pre-process data to be used in ML models. This lambda
Transform categorical variables in boolean variables, and
complete missing data

## Pre-requisites
A config.json file in meta folder:

```json
{
  "num_of_columns": int,
  "columns": [
    {
      "name": "name of column",
      "variable": "continues/discrete/categorical/Binary",
      "flow": "in/out"
    }
    ],
  "method_of_normalization": "standardization/normalization"
}
```

## Setup:
```shell
    make venv
    make setup
```

## Run:

```shell
    make run
```


## Deploy:
```shell
    make full_deploy
```

or

```shell
    make buid
    make deploy
```