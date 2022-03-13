"""Script used for automating interest on loans."""
from finance.monzo_automation import MonzoAutomation

MonzoAutomation().update_interest()
