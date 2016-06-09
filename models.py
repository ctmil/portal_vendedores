# -*- coding: utf-8 -*-
from openerp import models, api, fields


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
