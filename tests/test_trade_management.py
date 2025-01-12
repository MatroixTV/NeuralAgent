# Test Trade Management

from trade_management.trade_executor import TradeExecutor
from trade_management.risk_manager import RiskManager
from trade_management.trailing_stop import TrailingStopManager

def test_trade_executor():
    """
    Test the TradeExecutor class for buy/sell and close operations.
    """
    executor = TradeExecutor(symbol="EURUSD")
    executor.open_buy(lot_size=0.1, stop_loss=50, take_profit=100)
    executor.open_sell(lot_size=0.1, stop_loss=50, take_profit=100)
    executor.close_position(position_id=1)

def test_risk_manager():
    """
    Test the RiskManager class for calculating lot size.
    """
    risk_manager = RiskManager(account_balance=10000, risk_per_trade=1)
    lot_size = risk_manager.calculate_lot_size(stop_loss_pips=50, pip_value=10)
    print(f"Calculated Lot Size: {lot_size}")

def test_trailing_stop_manager():
    """
    Test the TrailingStopManager class for updating stop-loss.
    """
    trailing_manager = TrailingStopManager(atr_multiplier=1.5)
    new_stop_loss = trailing_manager.update_stop_loss(
        position_id=1, current_price=1.1050, atr_value=0.0015, is_buy=True
    )
    print(f"New Stop-Loss: {new_stop_loss}")

# Run tests
def test_trade_management():
    test_trade_executor()
    test_risk_manager()
    test_trailing_stop_manager()

test_trade_management()
