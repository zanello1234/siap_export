from odoo import api, fields, models, _
from odoo.exceptions import UserError
import base64
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)

class SiapExportWizard(models.TransientModel):
    _name = 'siap.export.wizard'
    _description = 'SIAP Export Wizard'

    export_type = fields.Selection([
        ('receivable', 'Accounts Receivable (Top Customers)'),
        ('payable', 'Accounts Payable (Top Suppliers)')
    ], string='Export Type', default='receivable')
    export_date = fields.Date('Export Date', default=fields.Date.context_today)
    partner_preview_ids = fields.One2many('siap.export.partner.line', 'wizard_id', string='Partners Preview')
    txt_file = fields.Binary('TXT File')
    txt_filename = fields.Char('Filename')
    format_type = fields.Selection([
        ('fixed', 'Fixed Width (SIAP Format)'),
        ('delimited', 'Pipe Delimited')
    ], string='File Format', default='fixed')
    
    def action_preview(self):
        """Generate preview data and show it in the preview form"""
        self.ensure_one()
        self._generate_preview_data()
        
        action = {
            'name': _('SIAP Export Preview'),
            'type': 'ir.actions.act_window',
            'res_model': 'siap.export.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'view_id': self.env.ref('siap_export.view_siap_export_preview_form').id,
            'target': 'new',
            'flags': {'mode': 'readonly'},
        }
        return action
        
    def action_back_to_wizard(self):
        """Return to the main wizard form"""
        self.ensure_one()
        return {
            'name': _('SIAP Export'),
            'type': 'ir.actions.act_window',
            'res_model': 'siap.export.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'view_id': self.env.ref('siap_export.view_siap_export_wizard').id,
            'target': 'new',
        }
    
    def _generate_preview_data(self):
        """Generate the preview data for top 20 partners"""
        self.ensure_one()
        
        # Clear existing preview lines
        self.partner_preview_ids.unlink()
        
        # Get top 20 partners based on export_type
        account_type = 'asset_receivable' if self.export_type == 'receivable' else 'liability_payable'
        
        # Updated SQL query for Odoo 17
        self.env.cr.execute("""
            SELECT aml.partner_id, SUM(aml.amount_residual) as total
            FROM account_move_line aml
            JOIN account_account aa ON aml.account_id = aa.id
            WHERE aa.account_type = %s
              AND aml.reconciled = FALSE
              AND aml.parent_state = 'posted'
              AND aml.date <= %s
            GROUP BY aml.partner_id
            ORDER BY total DESC
            LIMIT 20
        """, (account_type, self.export_date))
        
        result = self.env.cr.dictfetchall()
        
        # Create preview lines
        for i, line in enumerate(result, 1):
            if not line['partner_id']:
                continue
                
            partner = self.env['res.partner'].browse(line['partner_id'])
            
            self.env['siap.export.partner.line'].create({
                'wizard_id': self.id,
                'sequence': i,
                'partner_id': partner.id,
                'vat': partner.vat or '',
                'amount': line['total'],
                'currency_id': self.env.company.currency_id.id,
            })
    
    def action_export(self):
        """Export data to TXT file based on preview data with specific field widths"""
        self.ensure_one()
        
        if not self.partner_preview_ids:
            raise UserError(_("No data to export. Please generate preview first."))
        
        # Generate TXT content with specific field widths
        content = ""
        for line in self.partner_preview_ids:
            if self.format_type == 'fixed':
                # Format fields with specific widths
                vat = (line.vat or 'SIN CUIT').ljust(11)[:11]  # VAT/CUIT: 11 chars
                partner_name = line.partner_id.name.replace('\n', ' ').replace('\r', '')
                partner_name = partner_name.ljust(50)[:50]  # Name: 61 chars
                
                # Format amount: 15 chars (12 integer + decimal point + 2 decimals)
                amount_str = "{:015.2f}".format(abs(line.amount))
                
                # Combine fields with fixed widths (no separators)
                content += f"{vat}{partner_name}{amount_str}\r\n"
            else:
                # Pipe-delimited format
                formatted_amount = "{:.2f}".format(abs(line.amount))
                partner_name = line.partner_id.name.replace('|', ' ').replace('\n', ' ').replace('\r', '')
                vat = line.vat or 'SIN CUIT'
                
                content += f"{vat}|{partner_name}|{formatted_amount}\r\n"
        
        # Generate filename
        type_str = "CLIENTES" if self.export_type == 'receivable' else "PROVEEDORES"
        date_str = self.export_date.strftime('%Y%m%d')
        filename = f"SIAP_TOP20_{type_str}_{date_str}.txt"
        
        # Create binary file
        self.txt_file = base64.b64encode(content.encode('utf-8'))
        self.txt_filename = filename
        
        # Return the file for download
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content?model={self._name}&id={self.id}&field=txt_file&download=true&filename={filename}',
            'target': 'self',
        }

class SiapExportPartnerLine(models.TransientModel):
    _name = 'siap.export.partner.line'
    _description = 'SIAP Export Partner Line'
    _order = 'sequence, id'
    
    wizard_id = fields.Many2one('siap.export.wizard', string='Wizard', required=True)
    sequence = fields.Integer('Sequence', default=10)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    vat = fields.Char('VAT')
    amount = fields.Monetary('Amount', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True)