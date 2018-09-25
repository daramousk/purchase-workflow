# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
#    Copyright (c) 2015 ICTSTUDIO (www.ictstudio.eu).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class PurchaseOrderLine(models.Model):
    _inherit="purchase.order.line"


    @api.multi
    def get_cancel_procurements(self):
        _logger.debug("Cancel Procurement Orders")
        procurements_to_cancel = self.env['procurement.order'].search(
                [
                    ('purchase_line_id', 'in', self.ids),
                    ('state', 'not in', ['cancel','done'])
                ]
        )
        _logger.debug("Procurement Orders to Cancel: %s", procurements_to_cancel)
        return procurements_to_cancel

    @api.multi
    def action_cancel(self):
        _logger.debug("Cancel PO Lines")
        res = super(PurchaseOrderLine, self).action_cancel()

        cancel_procurements = self.get_cancel_procurements()
        try:
            _logger.debug("Cancel Procurements from PO Line: %s", cancel_procurements)
            cancel_procurements.write({'state': 'cancel'})
        except:
            _logger.error("Unable to Cancel Procurements: %s", cancel_procurements)
        return res