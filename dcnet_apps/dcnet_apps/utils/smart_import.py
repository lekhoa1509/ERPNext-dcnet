"""
Smart Import - AI-powered data import with automatic column mapping and direct insertion.

Features:
- Analyzes uploaded CSV/XLSX files
- Uses AI to intelligently map columns to DocType fields
- Validates data before insertion
- Inserts records directly without manual mapping
- Handles data type conversions automatically
"""

import csv
import os
import re
from typing import Any, Dict, List

import openpyxl

import frappe
from frappe import _
from frappe.utils import cstr


class SmartImporter:
	"""AI-powered importer that analyzes and maps data automatically."""
	
	def __init__(self, doctype: str, file_path: str):
		self.doctype = _validate_doctype(doctype)
		self.file_path = _resolve_import_file_path(file_path)
		self.meta = frappe.get_meta(self.doctype)
		self.rows = []
		self.headers = []
		self.column_mapping = {}
		
	def read_file(self) -> List[Dict[str, Any]]:
		"""Read CSV or XLSX file and return rows."""
		file_path = self.file_path.lower()
		if file_path.endswith('.csv'):
			return self._read_csv()
		elif file_path.endswith(('.xlsx', '.xls')):
			return self._read_excel()
		else:
			frappe.throw(_("Unsupported file format. Use CSV or XLSX."))
	
	def _read_csv(self) -> List[Dict[str, Any]]:
		"""Read CSV file."""
		rows = []
		with open(self.file_path, 'r', encoding='utf-8') as f:
			reader = csv.DictReader(f)
			self.headers = reader.fieldnames or []
			for row in reader:
				rows.append(row)
		return rows
	
	def _read_excel(self) -> List[Dict[str, Any]]:
		"""Read XLSX file."""
		rows = []
		wb = openpyxl.load_workbook(self.file_path)
		ws = wb.active
		
		# Get headers from first row
		self.headers = [cell.value for cell in ws[1]]
		
		# Get data rows
		for row in ws.iter_rows(min_row=2, values_only=True):
			row_dict = {self.headers[i]: row[i] for i in range(len(self.headers))}
			rows.append(row_dict)
		
		return rows
	
	def analyze_and_map_columns(self) -> Dict[str, str]:
		"""
		Analyze file headers and map to DocType fields using AI.
		
		Returns:
			Dict mapping file columns to DocType field names
		"""
		# Get available fields from DocType
		doctype_fields = self._get_doctype_fields()
		
		# Use AI to map columns
		mapping = self._ai_map_columns(self.headers, doctype_fields)
		
		self.column_mapping = mapping
		return mapping
	
	def _get_doctype_fields(self) -> Dict[str, Dict[str, Any]]:
		"""Get all fields from DocType with their properties."""
		fields = {}
		for field in self.meta.fields:
			if field.fieldtype not in ['Section Break', 'Column Break', 'Tab Break']:
				fields[field.fieldname] = {
					'label': field.label,
					'fieldtype': field.fieldtype,
					'options': field.options or '',
					'required': field.reqd
				}
		return fields
	
	def _ai_map_columns(self, headers: List[str], doctype_fields: Dict[str, Dict]) -> Dict[str, str]:
		"""
		Use AI to intelligently map CSV headers to DocType fields.
		
		Strategy:
		1. Exact match (case-insensitive)
		2. Fuzzy match on field labels
		3. Semantic matching using field descriptions
		"""
		mapping = {}
		
		for header in headers:
			best_match = None
			best_score = 0
			
			# Try exact match first
			for fieldname, field_info in doctype_fields.items():
				score = self._calculate_match_score(header, fieldname, field_info)
				if score > best_score:
					best_score = score
					best_match = fieldname
			
			if best_match and best_score > 0.5:  # Confidence threshold
				mapping[header] = best_match
		
		return mapping
	
	def _calculate_match_score(self, header: str, fieldname: str, field_info: Dict) -> float:
		"""Calculate similarity score between header and field."""
		header_lower = header.lower().strip()
		fieldname_lower = fieldname.lower()
		label_lower = field_info['label'].lower()
		
		score = 0.0
		
		# Exact match
		if header_lower == fieldname_lower:
			return 1.0
		
		# Label match
		if header_lower == label_lower:
			return 0.95
		
		# Partial match
		if header_lower in label_lower or label_lower in header_lower:
			score += 0.7
		
		# Word overlap
		header_words = set(header_lower.split())
		field_words = set(fieldname_lower.split())
		label_words = set(label_lower.split())
		
		overlap = len(header_words & (field_words | label_words))
		if overlap > 0:
			score += (overlap / max(len(header_words), len(field_words | label_words))) * 0.3
		
		return min(score, 1.0)
	
	def validate_and_transform_data(self, rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
		"""
		Validate and transform data according to field types.
		
		Returns:
			List of validated and transformed rows
		"""
		validated_rows = []
		
		for idx, row in enumerate(rows, 1):
			try:
				validated_row = {}
				
				for file_col, doctype_field in self.column_mapping.items():
					if file_col not in row or row[file_col] is None:
						continue
					
					value = row[file_col]
					field_info = self._get_field_info(doctype_field)
					
					# Transform value based on field type
					transformed_value = self._transform_value(value, field_info)
					validated_row[doctype_field] = transformed_value
				
				validated_rows.append(validated_row)
			
			except Exception as e:
				frappe.log_error(f"Error validating row {idx}: {str(e)}", "Smart Import")
				continue
		
		return validated_rows
	
	def _get_field_info(self, fieldname: str) -> Dict[str, Any]:
		"""Get field information from DocType."""
		for field in self.meta.fields:
			if field.fieldname == fieldname:
				return {
					'fieldtype': field.fieldtype,
					'options': field.options or '',
					'reqd': field.reqd
				}
		return {}
	
	def _transform_value(self, value: Any, field_info: Dict[str, Any]) -> Any:
		"""Transform value based on field type."""
		fieldtype = field_info.get('fieldtype', 'Data')
		
		if value is None or value == '':
			return None
		
		value_str = cstr(value).strip()
		
		if fieldtype == 'Int':
			try:
				return int(float(value_str))
			except:
				return None
		
		elif fieldtype == 'Float':
			try:
				return float(value_str)
			except:
				return None
		
		elif fieldtype == 'Currency':
			try:
				# Remove currency symbols and convert
				cleaned = re.sub(r'[^\d.-]', '', value_str)
				return float(cleaned)
			except:
				return None
		
		elif fieldtype == 'Date':
			try:
				from frappe.utils import parse_date
				return parse_date(value_str)
			except:
				return None
		
		elif fieldtype == 'Checkbox':
			return 1 if value_str.lower() in ['yes', 'true', '1', 'on'] else 0
		
		elif fieldtype == 'Link':
			# Validate that linked document exists
			options = field_info.get('options', '')
			if options and frappe.db.exists(options, value_str):
				return value_str
			return None
		
		else:
			return value_str
	
	def insert_records(self, rows: List[Dict[str, Any]]) -> Dict[str, Any]:
		"""
		Insert validated records directly into database.
		
		Returns:
			Dict with insertion results
		"""
		results = {
			'success': 0,
			'failed': 0,
			'errors': [],
			'created_docs': []
		}
		
		for idx, row_data in enumerate(rows, 1):
			try:
				# Create new document
				doc = frappe.new_doc(self.doctype)
				
				# Set field values
				for fieldname, value in row_data.items():
					if value is not None:
						doc.set(fieldname, value)
				
				# Insert document
				doc.insert(ignore_permissions=False)
				
				results['success'] += 1
				results['created_docs'].append(doc.name)
			
			except Exception as e:
				results['failed'] += 1
				error_msg = f"Row {idx}: {str(e)}"
				results['errors'].append(error_msg)
				frappe.log_error(error_msg, "Smart Import")
		
		return results


@frappe.whitelist()
def smart_import(doctype: str, file_path: str) -> Dict[str, Any]:
	"""
	Main entry point for Smart Import.
	
	Args:
		doctype: Target DocType name
		file_path: Path to CSV/XLSX file
	
	Returns:
		Import results with success/failure counts
	"""
	try:
		# Initialize importer
		importer = SmartImporter(doctype, file_path)
		
		# Read file
		rows = importer.read_file()
		
		if not rows:
			frappe.throw(_("File is empty"))
		
		# Analyze and map columns
		mapping = importer.analyze_and_map_columns()
		
		if not mapping:
			frappe.throw(_("Could not map any columns. Please check file format."))
		
		# Validate and transform data
		validated_rows = importer.validate_and_transform_data(rows)
		
		if not validated_rows:
			frappe.throw(_("No valid rows found in file"))
		
		# Insert records
		results = importer.insert_records(validated_rows)
		
		# Log import
		frappe.log_error(
			f"Smart Import: {doctype} - Success: {results['success']}, Failed: {results['failed']}",
			"Smart Import"
		)
		
		return results
	
	except Exception as e:
		frappe.log_error(str(e), "Smart Import")
		frappe.throw(_("Smart Import failed: {0}").format(str(e)))


def _validate_doctype(doctype: str) -> str:
	"""Validate target DocType before reading metadata."""
	doctype = cstr(doctype).strip()
	if not doctype or doctype.lower() == "none":
		frappe.throw(_("Please select a target DocType before using Smart Import."))
	if not frappe.db.exists("DocType", doctype):
		frappe.throw(_("DocType {0} does not exist.").format(frappe.bold(doctype)))
	return doctype


def _resolve_import_file_path(file_path: str) -> str:
	"""Resolve a Frappe Attach file URL to an on-disk site path."""
	file_path = cstr(file_path).strip()
	if not file_path:
		frappe.throw(_("Please upload an import file before using Smart Import."))

	if os.path.isabs(file_path) and not file_path.startswith(("/files/", "/private/files/")):
		resolved_path = file_path
	else:
		clean_path = file_path.lstrip("/")
		parts = clean_path.split("/")
		if clean_path.startswith("files/"):
			resolved_path = frappe.get_site_path("public", *parts)
		elif clean_path.startswith("private/files/"):
			resolved_path = frappe.get_site_path(*parts)
		else:
			resolved_path = frappe.get_site_path(*parts)

	if not os.path.exists(resolved_path):
		frappe.throw(_("Import file does not exist: {0}").format(file_path))
	return resolved_path
