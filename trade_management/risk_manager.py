class RiskManager:
    """
    Manages risk, including position sizing and stop-loss calculations.
    """

    def __init__(self, account_balance, risk_per_trade):
        """
        Initialize the risk manager.

        :param account_balance: Account balance in currency
        :param risk_per_trade: Risk per trade as a percentage (e.g., 1 for 1%)
        """
        self.account_balance = account_balance
        self.risk_per_trade = risk_per_trade

    def calculate_lot_size(self, stop_loss_pips, pip_value):
        """
        Calculate the lot size for a trade.

        :param stop_loss_pips: Stop-loss in pips
        :param pip_value: Value of one pip in the account's base currency
        :return: Lot size
        """
        risk_amount = (self.risk_per_trade / 100) * self.account_balance
        lot_size = risk_amount / (stop_loss_pips * pip_value)
        return round(lot_size, 2)
