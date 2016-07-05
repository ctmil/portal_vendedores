# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
from lxml import etree

from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _
from openerp.tools import float_compare
from openerp.report import report_sxw
import openerp


class account_voucher(osv.osv):
	_inherit = 'account.voucher'

	def proforma_voucher(self, cr, uid, ids, context=None):
		for voucher_id in ids:
			voucher = self.pool.get('account.voucher').browse(cr,uid,voucher_id)
        		import pdb;pdb.set_trace()
			if voucher.voucher_type == 'receipt':
				if voucher.line_dr_ids:
					raise osv.except_osv(_('Accion invalida!'),\
						 _('Se seleccionaron debitos en pagos de clientes.'))					
			else:
				if voucher.line_cr_ids:
					raise osv.except_osv(_('Accion invalida!'),\
						 _('Se seleccionaron creditos en pagos a proveedores.'))					
	        return  super(account_voucher,self).proforma_voucher(cr,uid,ids,context)

account_voucher()
