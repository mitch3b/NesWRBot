#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Util class for making a speedrun time human readible
"""
import datetime

def fromTotalSeconds(totalSeconds):
    if totalSeconds is None or totalSeconds == 0:
        raise RuntimeError("Invalid time in seconds: " + str(totalSeconds))

    formattedTime = str(datetime.timedelta(seconds=totalSeconds))
    # Above will return hours even if not present. don't want that
    formattedTime = _remove_prefix(formattedTime, "00:");
    formattedTime = _remove_prefix(formattedTime, "0:");
    formattedTime = _remove_prefix(formattedTime, "0");
    formattedTime = _remove_zeros_after_milliseconds(formattedTime);

    return formattedTime

def _remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text  # or whatever

def _remove_zeros_after_milliseconds(text):
    if "." in text:
        last_decimal_point_index = text.rfind(".")
        return text[:last_decimal_point_index + 4]

    return text
