##############################################################################
# Developed by: Shobhit Agarwal
# This Module is used for the external actions
# example: find balance from database.
##############################################################################

# Import Packages
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd
import Global_var

def extractBalance(person):
	'''
		This function is used to extract the available balance from the database.
		:param person
		:return: Balance
	'''
	try:
		cust_details = pd.read_excel('customer_data.xlsx', engine='openpyxl')
	except Exception as err:
		print('err: ', err)
	balance = cust_details[cust_details['customer_name'] == person.lower()].balance
	balance = balance.values[0]
	return balance

def extractLastTransactions(person):
	'''
		This function is used to extract the last 10 transactions from the database.
		:param person
		:return: transactions
	'''

	cust_details = pd.read_excel('transaction_details.xlsx', engine='openpyxl')
	transactions = cust_details[cust_details['customer_name'] == person.lower()].transaction
	transactions = transactions.values[0]
	return transactions

# To-Do Where model is unable to understand the intent of a speaker from the pre-defined intents.
class MyFallback(Action):

	def name(self) -> Text:
		return "action_my_fallback"

	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		dispatcher.utter_message(template="Sorry! I can't understand, please say again")
		return []

class PersonName(Action):

	def name(self) -> Text:
		return "action_send_name"

	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		person = tracker.get_slot('person')
		Global_var.person = person
		try:
			return person
		except:
			return []

class ActionSendBalance(Action):

	def name(self) -> Text:
		return "action_send_balance"

	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

		# Find the slots value
		person = tracker.get_slot('person')
		mobile = tracker.get_slot('mobile')
		Global_var.person = person
		Global_var.mobile = mobile
		try:
			balance = extractBalance(person)
			# Send message from bot to the user.
			dispatcher.utter_message(text="Thank you Mr. " + str(person) + ", Your available balance is " + str(balance))
		except:
			# Send message from bot to the user.
			dispatcher.utter_message(text="Thank you Mr. "+str(person)+" but your details doesn't match with the database.")
		return []
