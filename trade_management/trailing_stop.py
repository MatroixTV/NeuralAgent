class TrailingStopManager:
    """
    Dynamically manages trailing stops for active positions.
    """

    def __init__(self, atr_multiplier):
        """
        Initialize the trailing stop manager.

        :param atr_multiplier: Multiplier for ATR-based trailing stop
        """
        self.atr_multiplier = atr_multiplier

    def update_stop_loss(self, position_id, current_price, atr_value, is_buy):
        """
        Update the stop-loss for an active position.

        :param position_id: ID of the position to update
        :param current_price: Current market price
        :param atr_value: ATR value for volatility
        :param is_buy: Whether the position is a buy order
        :return: New stop-loss price
        """
        trailing_distance = self.atr_multiplier * atr_value
        new_stop_loss = (
            current_price - trailing_distance if is_buy else current_price + trailing_distance
        )
        print(f"Updated Stop-Loss for Position {position_id}: {new_stop_loss}")
        return new_stop_loss
