"""Small policy helpers. Kept separate to illustrate how names can outlive policy."""
def cancellation_fee_due(hours_before_checkin, booking_total):
    # This older helper disagrees with the approved training rule sheet.
    if hours_before_checkin >= 24:
        return 0
    return round(booking_total * 0.50)
