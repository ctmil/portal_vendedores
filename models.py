# -*- coding: utf-8 -*-
from openerp import models, api, fields, exceptions
from openerp.exceptions import ValidationError

class sale_order(models.Model):
	_inherit = "sale.order"

	to_process = fields.Boolean(string='Confirmar Pedido',default=False)

	@api.one
	def action_to_process(self):
		self.ensure_one()
		if self.state != 'draft':
			return None
		if self.to_process:	
			self.to_process = False
		else:
			self.to_process = True

class account_journal(models.Model):
	_inherit = 'account.journal'

	is_retention = fields.Boolean(string='Es retencion', default=False)

class account_move_line(models.Model):
	_inherit = 'account.move.line'

	@api.one
	def _compute_saldo(self):
		saldo = 0
		if self.account_id.id == 11:
			move_lines = self.env['account.move.line'].search([('id','<=',self.id),('account_id','=',11),\
					('partner_id','=',self.partner_id.id)],order='id asc')
			for line in move_lines:
				if line.debit > 0:
					saldo = saldo + line.debit
				if line.credit > 0:
					saldo = saldo - line.credit
			self.saldo = saldo
		else:
			self.saldo = 0

	saldo = fields.Float(string='Saldo',compute=_compute_saldo)


class account_voucher(models.Model):
	_inherit = 'account.voucher'

	@api.model
	def create(self,vals):
		if vals['journal_id']:
			journal = self.env['account.journal'].browse(vals['journal_id'])
			if journal.is_retention:
				if not vals['reference']:
					raise exceptions.ValidationError('No ingreso el nro de certificado de retencion')
				if vals['reference'] == '':
					raise exceptions.ValidationError('No ingreso el nro de certificado de retencion')
		return super(account_voucher, self).create(vals)
	
	@api.multi
	def write(self,vals):
		if 'journal_id' in vals:
			if vals['journal_id']:
				journal = self.env['account.journal'].browse(vals['journal_id'])
				if journal.is_retention:
					if not vals['reference']:
						raise exceptions.ValidationError('No ingreso el nro de certificado de retencion')
					if vals['reference']:
						raise exceptions.ValidationError('No ingreso el nro de certificado de retencion')
		return super(account_voucher, self).write(vals)


class account_invoice(models.Model):
	_inherit = 'account.invoice'
	
	@api.one
	@api.constrains('supplier_invoice_number')
	def check_invoice_number(self):
		if self.supplier_invoice_number:
			invoices = self.env['account.invoice'].search([('partner_id','=',self.partner_id.id),\
					('type','=','in_invoice'),('supplier_invoice_number','=',self.supplier_invoice_number)])
			if len(invoices) > 1:
			        raise ValidationError("Fields name and description must be different")

