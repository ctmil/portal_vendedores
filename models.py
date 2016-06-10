# -*- coding: utf-8 -*-
from openerp import models, api, fields, exceptions


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
