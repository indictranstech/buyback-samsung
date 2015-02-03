# Copyright (c) 2013, samsungapp and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils.email_lib import sendmail
from frappe.utils import nowdate, cstr, flt, now, getdate, add_months,formatdate,cstr

class BuyBackRequisition(Document):
	pass



@frappe.whitelist()
def test(BuyBackRequisition, method):
	frappe.errprint("BuyBackRequisition.name")
	frappe.errprint(BuyBackRequisition.customer_acceptance)


@frappe.whitelist()
def save(BuyBackRequisition, method):
	frappe.errprint("in the save")
	frappe.errprint(BuyBackRequisition.customer_acceptance)
	if BuyBackRequisition.customer_acceptance=='Yes':
		po = frappe.new_doc('Purchase Order')
		po.supplier= 'Slot buy back program'
		po.naming_series="PO-BB-"
		po.buy_back_requisition_ref=BuyBackRequisition.name
		poc = po.append('po_details', {})
		poc.item_code=BuyBackRequisition.item_code
		poc.schedule_date=nowdate()
		poc.rate=BuyBackRequisition.offered_price
		po.docstatus=1
		po.insert(ignore_permissions=True)
		frappe.errprint(po.name)
		send_device_recv_email(BuyBackRequisition, method)



@frappe.whitelist()
def get_device_active_Details(active):
	#frappe.errprint(active)
	if active=='Yes':
		active_percentage=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
					and field='device_active_yes_percentage' """)
	elif active=='No':
		active_percentage=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
					and field='device_active_no_percentage' """)
	else:
		pass

	if len(active_percentage) >0:
		return active_percentage[0][0]
	else:

		return 0

@frappe.whitelist()
def get_functional_defects_details(functional_defects,active):
	frappe.errprint(functional_defects)
	frappe.errprint(active)
	functional_value=[]
	if active=='Yes':
		if functional_defects=='Yes':
			functional_value=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='active_yes_percentage' """)
		elif functional_defects=='No':
			functional_value=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='active_no_percentage' """)
			frappe.errprint(functional_value)	
		else:
			pass

	elif active=='No':
		if functional_defects=='Yes':
			functional_value=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='deactivate_yes_percentage' """)
		elif functional_defects=='No':
			functional_value=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='deactivate_no_percentage' """)
		else:
			pass
			

	if len(functional_value)>0:
		return functional_value[0][0]
	else:
		return 0

@frappe.whitelist()
def get_condition_of_screen(screen_condition,active):
	frappe.errprint(screen_condition)
	screen=[]
	if active=='Yes':
		frappe.errprint("in active yes")
		if screen_condition=='Broken Screen':
			screen=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='a_broken_screen' """)
		elif screen_condition=='Poor':
			screen=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='a_poor_screen' """)
		elif screen_condition=='Just OK':
			screen=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='a_just_ok_screen' """)
		elif screen_condition=='Excellent':
			screen=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='a_excellent_screen' """)
	elif active=='No':
		if screen_condition=='Broken Screen':
			screen=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='deactive_broken_screen' """)
		elif screen_condition=='Poor':
			screen=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='deactive_poor_screen' """)
		elif screen_condition=='Just OK':
			screen=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='deactive_just_ok_screen' """)
		elif screen_condition=='Excellent':
			screen=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='deactive_excellent_screen' """)
	else:
		pass

	if len(screen)>0:
		return screen[0][0]
	else:
		return 0

@frappe.whitelist()
def get_condition_of_device_body(device_body,active):
	body_condition=[]
	if active=='Yes':
		if device_body=='Poor':
			body_condition=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='a_poor_body_condition' """)
		elif device_body=='Just OK':
			body_condition=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='just_ok_body' """)
		elif device_body=='Excellent':
			body_condition=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='excellent_body' """)
	elif active=='No':
		if device_body=='Poor':
			body_condition=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='deactive_poor_body' """)
		elif device_body=='Just OK':
			body_condition=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='deactive_just_ok_body' """)
		elif device_body=='Excellent':
			body_condition=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='deactive_excellent' """)
	else:
		pass

	if len(body_condition)>0:
		return body_condition[0][0]
	else:
		return 0


@frappe.whitelist()
def get_accessories_details(accessories,active):
	accessories_details=[]
	if active=='Yes':
		if accessories=='Yes':
			accessories_details=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='accessories_yes_percentage' """)
		elif accessories=='No':
			accessories_details=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='accessories_no_percentage' """)

	elif active=='No':
		if accessories=='Yes':
			accessories_details=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='deactive_yes_accessories' """)
		elif accessories=='No':
			accessories_details=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='deactive_no_accessories' """)

	else:
		pass

	if len(accessories_details)>0:
		return accessories_details[0][0]
	else:
		return 0


@frappe.whitelist()
def get_capacity(capacity,active):
	capacity_details=[]
	if active=='Yes':
		if capacity=='8GB':
			capacity_details=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='a_percentage' """)
			frappe.errprint(capacity_details)
		elif capacity=='16GB':
			capacity_details=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='a_one_percentage' """)
		elif capacity=='32GB':
			capacity_details=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='a_two_percentage' """)
		elif capacity=='64GB':
			capacity_details=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='a_tr_percentage' """)
		elif capacity=='128GB':
			capacity_details=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='a_fr_percentage' """)
		elif capacity=='N/A':
			capacity_details=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='not_applicable_percentage' """)
	elif active=='No':
		if capacity=='8GB':
			capacity_details=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='deactive_8gb' """)
		elif capacity=='16GB':
			capacity_details=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='deactive_16gb' """)
		elif capacity=='32GB':
			capacity_details=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='deactive_32gb' """)
		elif capacity=='64GB':
			capacity_details=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='deactive_64gb' """)
		elif capacity=='128GB':
			capacity_details=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='deactive_128gb' """)
		elif capacity=='N/A':
			capacity_details=frappe.db.sql("""select ifnull(value,0) from `tabSingles` where doctype='Deduction Percentage Criteria'
						and field='deactive_na' """)
	if len(capacity_details)>0:
		return capacity_details[0][0]
	else:
		return 0


# @frappe.whitelist()
def send_device_recv_email(BuyBackRequisition, method):
	recipients=[]
	expiry_date=''
	if BuyBackRequisition.email_id:
		recipients.append(BuyBackRequisition.email_id)
	recipient=frappe.db.sql("""select parent from `tabUserRole` where role in('MSE','Slot Cashier','Slot Representative')""",as_dict=1,debug=1)
	if recipient:
		for resp in recipient:
			recipients.append(resp['parent'])
	if recipients:
		subject = "Device Received"
		message ="""<h3>Dear </h3><p>We received your device at Matrix store, below are the details</p>
		<p>Device Received :%s</p>
		<p>Received Date:%s </p>
		<p>Offered Price:%s</p>
		<p>Voucher will be sent to you via PIN. PIN will be sent to you in a separate email & sms correspondence.</p>
		<p>Thank You,</p>
		""" %(BuyBackRequisition.item_name,formatdate(BuyBackRequisition.creation),BuyBackRequisition.offered_price)
		sendmail(recipients, subject=subject, msg=message)	










