from fastapi import Body, Query

model_version = Query(None, alias="modelVersion", description="Model version of diabetes predictor.")
input = Body(..., alias="input", description="Input to the diabetes prediction model.")
include_model_version = Query(False, alias="includeModelVersion", description="If true, model version will be included in the response.")
include_input = Query(False, alias="includeInput", description="If true, input will be included in the response.")