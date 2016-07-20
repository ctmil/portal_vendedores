# -*- coding: utf-8 -*-
from openerp import models, api, fields, exceptions
from openerp.exceptions import ValidationError

class sale_order(models.Model):
	_inherit = "sale.order"

	@api.one
	def _compute_number_lines(self):
		return_value = 0
		for line in self.order_line:
			return_value = return_value + 1
		self.number_lines = return_value

	@api.one
	def _compute_percepciones(self):
		return_value = 0
		if self.partner_id.perception_ids:
			for perception in self.partner_id.perception_ids:
				return_value = return_value + self.amount_untaxed * (perception.percent / 100)
		self.monto_percepciones = return_value

	@api.one
	def _compute_con_percepciones(self):
		self.monto_con_percepciones = self.amount_total + self.monto_percepciones

	to_process = fields.Boolean(string='Confirmar Pedido',default=False)
	balance_ok = fields.Boolean(string='OK Cta Cte',default=False)
	figures_ok = fields.Boolean(string='OK Precios/Cantidades',default=False)
	number_lines = fields.Integer(string='Cantidad de lineas',compute=_compute_number_lines)
	monto_percepciones = fields.Float(string='Monto Percepciones',compute=_compute_percepciones)
	monto_con_percepciones = fields.Float(string='Total con Percepciones',compute=_compute_con_percepciones)

	@api.one
	def action_figures_ok(self):
		self.ensure_one()
		if self.state != 'draft':
			return None
		if not self.to_process:
			raise exceptions.ValidationError('Primero el vendedor debe marcar el pedido como confirmado')
		if self.figures_ok:	
			self.figures_ok = False
		else:
			self.figures_ok = True

	@api.one
	def action_to_process(self):
		self.ensure_one()
		if self.state != 'draft':
			return None
		if self.to_process:	
			self.to_process = False
		else:
			self.to_process = True

	@api.one
	def action_balance_ok(self):
		self.ensure_one()
		if self.state != 'draft':
			return None
		if not self.to_process:
			raise exceptions.ValidationError('Primero el vendedor debe marcar el pedido como confirmado')
		if not self.figures_ok:
			raise exceptions.ValidationError('Primero debe indicarse que los Precios/Cantidades estan OK')
		if self.balance_ok:	
			self.balance_ok = False
		else:
			self.balance_ok = True


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
				if not vals['fecha_retencion']:
					raise exceptions.ValidationError('No ingreso la fecha de retencion')
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
					if not vals['fecha_retencion']:
						raise exceptions.ValidationError('No ingreso la fecha de retencion')
		return super(account_voucher, self).write(vals)

	fecha_retencion = fields.Date(string='Fecha Retencion')

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



class sale_order_line(osv.osv):
        _inherit = 'sale.order.line'


        """     
        def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,uom=False, qty_uos=0,\
                 uos=False, name='', partner_id=False,lang=False, update_tax=True, date_order=False,\
                 packaging=False, fiscal_position=False, flag=False, context=None):
                import pdb;pdb.set_trace()
                return super(sale_order_line, self).product_id_change(cr,uid,ids,pricelist,product,qty,uom,qty_uos,uos,name,\
                                partner_id,lang,update_tax,date_order,packaging,fiscal_position,flag,context)
        """


        def _check_routing(self, cr, uid, ids, product, warehouse_id, context=None):
                return True

