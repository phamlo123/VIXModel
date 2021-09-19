import Option
import processing_featuring


# This function calculates the value of VIX from the selected options price
def vix_calculation (list_of_option):
    vix = 0
    k_delta = processing_featuring.strikeDelta

    for item in list_of_option:
        price = item.Option.quote
        strike = item.Option.strike
        portion = (2 * k_delta) / (strike ** 2) * price

        vix += portion

    return vix
