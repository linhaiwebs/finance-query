from stock_indicators import indicators
from typing_extensions import OrderedDict

from src.schemas.analysis import MACDData, Analysis, ADXData, AROONData, BBANDSData, OBVData, SuperTrendData, \
    IchimokuData
from src.schemas.time_series import TimePeriod, Interval
from src.services.get_historical import get_historical_quotes


async def get_macd(symbol: str, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9):
    quotes = await get_historical_quotes(symbol, timePeriod=TimePeriod.SIX_MONTHS, interval=Interval.DAILY)
    results = indicators.get_macd(quotes, fast_periods=round(fast_period, 2), slow_periods=round(slow_period, 2),
                                  signal_periods=signal_period)

    indicator_data = {result.date.date(): MACDData(value=result.macd, signal=result.signal) for
                      result in results if result.macd is not None and result.signal is not None}
    indicator_data = OrderedDict(sorted(indicator_data.items(), reverse=True))
    return Analysis(indicators=indicator_data)


async def get_adx(symbol: str, period: int = 14):
    quotes = await get_historical_quotes(symbol, timePeriod=TimePeriod.SIX_MONTHS, interval=Interval.DAILY)
    results = indicators.get_adx(quotes, lookback_periods=period)
    indicator_data = {result.date.date(): ADXData(value=round(result.adx, 2)) for result in results if
                      result.adx is not None}
    indicator_data = OrderedDict(sorted(indicator_data.items(), reverse=True))
    return Analysis(indicators=indicator_data)


async def get_aroon(symbol: str, period: int = 25):
    quotes = await get_historical_quotes(symbol, timePeriod=TimePeriod.SIX_MONTHS, interval=Interval.DAILY)
    results = indicators.get_aroon(quotes, lookback_periods=period)
    indicator_data = {
        result.date.date(): AROONData(aroon_up=round(result.aroon_up, 2), aroon_down=round(result.aroon_down, 2)) for
        result in results if result.aroon_up is not None and result.aroon_down is not None}
    indicator_data = OrderedDict(sorted(indicator_data.items(), reverse=True))
    return Analysis(indicators=indicator_data)


async def get_bbands(symbol: str, period: int = 14, std_dev: int = 2):
    quotes = await get_historical_quotes(symbol, timePeriod=TimePeriod.SIX_MONTHS, interval=Interval.DAILY)
    results = indicators.get_bollinger_bands(quotes, lookback_periods=period, standard_deviations=std_dev)
    indicator_data = {
        result.date.date(): BBANDSData(upper_band=round(result.upper_band, 2), lower_band=round(result.lower_band, 2))
        for result in results if result.upper_band is not None and result.lower_band is not None}
    indicator_data = OrderedDict(sorted(indicator_data.items(), reverse=True))
    return Analysis(indicators=indicator_data)


async def get_obv(symbol: str, sma_periods: int = None):
    quotes = await get_historical_quotes(symbol, timePeriod=TimePeriod.SIX_MONTHS, interval=Interval.DAILY)
    results = indicators.get_obv(quotes, sma_periods=sma_periods)
    indicator_data = {result.date.date(): OBVData(value=round(result.obv, 2)) for result in results if
                      result.obv is not None}
    indicator_data = OrderedDict(sorted(indicator_data.items(), reverse=True))
    return Analysis(indicators=indicator_data)


async def get_super_trend(symbol: str, period: int = 14, multiplier: int = 3):
    quotes = await get_historical_quotes(symbol, timePeriod=TimePeriod.SIX_MONTHS, interval=Interval.DAILY)
    results = indicators.get_super_trend(quotes, lookback_periods=period, multiplier=multiplier)
    for r in results:
        print(r.date, r.super_trend, r.upper_band, r.lower_band)
    indicator_data = {
        result.date.date(): SuperTrendData(value=round(result.super_trend, 2),
                                           trend="DOWN" if result.upper_band else "UP"
                                           )
        for result in results if result.super_trend is not None}
    indicator_data = OrderedDict(sorted(indicator_data.items(), reverse=True))
    return Analysis(indicators=indicator_data)


async def get_ichimoku(symbol: str, tenkan_period: int = 9, kijun_period: int = 26, senkou_period: int = 52,
                       senkou_offset: int = 26, chikou_offset: int = 26):
    quotes = await get_historical_quotes(symbol, timePeriod=TimePeriod.SIX_MONTHS, interval=Interval.DAILY)
    results = indicators.get_ichimoku(
        quotes,
        tenkan_periods=tenkan_period,
        kijun_periods=kijun_period,
        senkou_b_periods=senkou_period,
        senkou_offset=senkou_offset, chikou_offset=chikou_offset
    )
    for r in results:
        print(r.date, r.tenkan_sen, r.kijun_sen, r.senkou_span_a, r.senkou_span_b, r.chikou_span)
    indicator_data = {
        result.date.date(): IchimokuData(
            tenkan_sen=round(result.tenkan_sen, 2) if result.tenkan_sen is not None else None,
            kijun_sen=round(result.kijun_sen, 2) if result.kijun_sen is not None else None,
            senkou_span_a=round(result.senkou_span_a, 2) if result.senkou_span_a is not None else None,
            senkou_span_b=round(result.senkou_span_b, 2) if result.senkou_span_b is not None else None,
            chikou_span=round(result.chikou_span, 2) if result.chikou_span is not None else None
        )
        for result in results
    }
    indicator_data = OrderedDict(sorted(indicator_data.items(), reverse=True))
    print(indicator_data)
    return Analysis(indicators=indicator_data)
