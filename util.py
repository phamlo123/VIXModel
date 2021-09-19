import Option
import processing_featuring

# get price of an option for using in VIX calculation using interpolation when maturity of desired option does not
# coincides with forecast horizon (30days)

forecast_horizon = processing_featuring.forecast_horizon


def get_price_using_interpolation (option1: Option, option2: Option):
    option1_price = option1.Option.quote
    option2_price = option2.Option.quote
    option1_time_to_mat = option1.Option.get_time_to_maturity ()
    option2_time_to_mat = option2.Option.get_time_to_maturity ()
    first_term = option1_price * (option2_time_to_mat - forecast_horizon) / (option2_time_to_mat - option1_time_to_mat)
    second_term = option2_price * (forecast_horizon - option1_time_to_mat) / (option2_time_to_mat - option1_time_to_mat)

    constructed_price = first_term + second_term

    return constructed_price


