"""Script used for automating populating newly found merchants."""
from finance.monzo_automation import MonzoAutomation

MonzoAutomation().populate_merchants(days=80)
