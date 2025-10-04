from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import base64
from datetime import datetime, date
import logging

_logger = logging.getLogger(__name__)

class SiapExportWizard(models.TransientModel):
    _name = 'siap.export.wizard'
    _description = 'SIAP Export Wizard'

    export_type = fields.Selection([
        ('receivable', 'Accounts Receivable (Top Customers)'),
        ('payable', 'Accounts Payable (Top Suppliers)')
    ], string='Export Type', default='receivable', required=True)
    
    export_date = fields.Date(
        'Export Date', 
        default=fields.Date.context_today,
        required=True,
        help="Select the cutoff date for the export. Only transactions up to this date will be included."
    )
    
    partner_preview_ids = fields.One2many(
        'siap.export.partner.line', 
        'wizard_id', 
        string='Partners Preview'
    )
    
    txt_file = fields.Binary('TXT File', readonly=True)
    txt_filename = fields.Char('Filename', readonly=True)
    
    format_type = fields.Selection([
        ('fixed', 'Fixed Width (SIAP Format)'),
        ('delimited', 'Pipe Delimited')
    ], string='File Format', default='fixed', required=True)
    
    company_id = fields.Many2one(
        'res.company', 
        string='Company', 
        default=lambda self: self.env.company,
        required=True
    )
    
    @api.constrains('export_date')
    def _check_export_date(self):
        """Validate export date is not in the future"""
        for record in self:
            if record.export_date > fields.Date.context_today(self):
                raise ValidationError(_('Export date cannot be in the future.'))
    
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
        
    def action_back(self):
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
        """Generate the preview data for top 20 partners - simplified approach"""
        self.ensure_one()
        
        # Clear existing preview lines
        self.partner_preview_ids.unlink()
        
        # Simplified approach - use ORM with clear logic
        if self.export_type == 'receivable':
            # For customers
            partner_domain = [
                ('customer_rank', '>', 0),
                ('is_company', '=', True)
            ]
            move_types = ['out_invoice']  # Start with just invoices
        else:
            # For suppliers
            partner_domain = [
                ('supplier_rank', '>', 0), 
                ('is_company', '=', True)
            ]
            move_types = ['in_invoice']  # Start with just bills
        
        # Get all potential partners
        partners = self.env['res.partner'].search(partner_domain)
        _logger.info(f"Found {len(partners)} total partners for {self.export_type}")
        
        partner_amounts = []
        
        for partner in partners:
            # Simple approach - get posted invoices
            moves = self.env['account.move'].search([
                ('partner_id', '=', partner.id),
                ('move_type', 'in', move_types),
                ('state', '=', 'posted'),
                ('invoice_date', '<=', self.export_date),
                ('company_id', '=', self.company_id.id)
            ])
            
            if moves:
                # Sum the total amounts
                total_amount = sum(move.amount_total for move in moves)
                
                if total_amount > 0:
                    partner_amounts.append({
                        'partner': partner,
                        'amount': total_amount
                    })
                    _logger.info(f"Partner {partner.name}: {total_amount}")
        
        _logger.info(f"Found {len(partner_amounts)} partners with amounts > 0")
        
        # Sort by amount descending and take top 20
        partner_amounts.sort(key=lambda x: x['amount'], reverse=True)
        top_20 = partner_amounts[:20]
        
        _logger.info(f"Creating preview for top {len(top_20)} partners")
        
        # Create preview lines
        for i, data in enumerate(top_20, 1):
            partner = data['partner']
            amount = data['amount']
            
            self.env['siap.export.partner.line'].create({
                'wizard_id': self.id,
                'sequence': i,
                'partner_id': partner.id,
                'vat': partner.vat or '',
                'amount': amount,
                'currency_id': self.company_id.currency_id.id,
            })
            _logger.info(f"Created line {i}: {partner.name} - {amount}")
        
        # If still no results, let's debug what we have
        if not top_20:
            _logger.warning("No partners found - debugging...")
            
            # Check if there are any moves at all
            all_moves = self.env['account.move'].search([
                ('move_type', 'in', move_types),
                ('state', '=', 'posted'),
                ('company_id', '=', self.company_id.id)
            ], limit=5)
            _logger.info(f"Sample moves found: {len(all_moves)}")
            for move in all_moves:
                _logger.info(f"Move: {move.name}, Partner: {move.partner_id.name if move.partner_id else 'None'}, Amount: {move.amount_total}")
            
            # Check if partners exist
            _logger.info(f"Sample partners: {[p.name for p in partners[:5]]}")
            
            # Check date filter
            _logger.info(f"Export date: {self.export_date}")
            _logger.info(f"Company: {self.company_id.name}")
    
    def action_export(self):
        """Export data to TXT file with enhanced security and validation for Odoo 18"""
        self.ensure_one()
        
        if not self.partner_preview_ids:
            raise UserError(_("No data to export. Please generate preview first."))
        
        try:
            # Generate TXT content with specific field widths
            content = ""
            total_records = 0
            total_amount = 0.0
            
            for line in self.partner_preview_ids:
                if self.format_type == 'fixed':
                    # Format fields with specific widths for SIAP compliance
                    vat = (line.vat or 'SIN CUIT').ljust(11)[:11]  # VAT/CUIT: 11 chars
                    partner_name = line.partner_id.name.replace('\n', ' ').replace('\r', '').replace('\t', ' ')
                    partner_name = partner_name.ljust(50)[:50]  # Name: 50 chars
                    
                    # Format amount: 15 chars (12 integer + decimal point + 2 decimals)
                    amount_str = "{:015.2f}".format(abs(line.amount))
                    
                    # Combine fields with fixed widths (no separators)
                    content += f"{vat}{partner_name}{amount_str}\r\n"
                else:
                    # Pipe-delimited format with improved data cleaning
                    formatted_amount = "{:.2f}".format(abs(line.amount))
                    partner_name = line.partner_id.name
                    # Clean partner name for delimited format
                    partner_name = partner_name.replace('|', ' ').replace('\n', ' ').replace('\r', '').replace('\t', ' ')
                    vat = line.vat or 'SIN CUIT'
                    
                    content += f"{vat}|{partner_name}|{formatted_amount}\r\n"
                
                total_records += 1
                total_amount += abs(line.amount)
            
            # Add summary footer
            content += f"\r\n# SUMMARY: {total_records} records, Total: {total_amount:.2f}\r\n"
            content += f"# Generated on: {fields.Datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\r\n"
            content += f"# Company: {self.company_id.name}\r\n"
            
            # Generate filename with improved naming convention
            type_str = "CLIENTES" if self.export_type == 'receivable' else "PROVEEDORES"
            date_str = self.export_date.strftime('%Y%m%d')
            timestamp = fields.Datetime.now().strftime('%H%M%S')
            filename = f"SIAP_TOP20_{type_str}_{date_str}_{timestamp}.txt"
            
            # Create binary file with UTF-8 encoding
            self.write({
                'txt_file': base64.b64encode(content.encode('utf-8')),
                'txt_filename': filename
            })
            
            _logger.info(f"SIAP export completed: {filename}, {total_records} records, {total_amount:.2f} total")
            
            # Return the file for download with improved URL
            return {
                'type': 'ir.actions.act_url',
                'url': f'/web/content?model={self._name}&id={self.id}&field=txt_file&download=true&filename={filename}',
                'target': 'self',
            }
            
        except Exception as e:
            _logger.error(f"Error during SIAP export: {str(e)}")
            raise UserError(_('Error during export: %s') % str(e))


class SiapExportPartnerLine(models.TransientModel):
    """Partner line for SIAP export wizard preview"""
    _name = 'siap.export.partner.line'
    _description = 'SIAP Export Partner Line'
    _order = 'sequence, id'
    
    wizard_id = fields.Many2one('siap.export.wizard', string='Wizard', required=True, ondelete='cascade')
    sequence = fields.Integer('Sequence', default=10)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    vat = fields.Char('VAT', help="Tax identification number")
    amount = fields.Monetary('Amount', required=True, help="Total amount for this partner")
    currency_id = fields.Many2one('res.currency', string='Currency', required=True)
    
    # Additional fields for better reporting
    partner_category_ids = fields.Many2many(related='partner_id.category_id', string='Partner Tags', readonly=True)
    partner_country_id = fields.Many2one(related='partner_id.country_id', string='Country', readonly=True)
    
    @api.depends('partner_id')
    def _compute_display_name(self):
        """Compute display name for better UX"""
        for record in self:
            if record.partner_id:
                record.display_name = f"{record.sequence:02d}. {record.partner_id.name} - {record.amount:,.2f}"
            else:
                record.display_name = "Unknown Partner"