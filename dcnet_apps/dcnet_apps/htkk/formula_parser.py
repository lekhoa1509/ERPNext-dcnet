"""
Parse formulas from XSD xs:documentation annotations.

Tổng cục thuế nhúng công thức tính toán trong documentation của mỗi element.
Ví dụ: "Thuế GTGT phát sinh trong kỳ ([36]=[35]-[25])"

Parser này trích xuất:
- Target: [36]
- Formula: [35]-[25]
- Dependencies: [35], [25]
"""

import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import Optional

XS_NS = "http://www.w3.org/2001/XMLSchema"
XS = f"{{{XS_NS}}}"


@dataclass
class FormulaField:
    """Represents a field with optional calculation formula."""
    element: str           # ct36
    indicator: str         # [36]
    label: str             # Thuế GTGT phát sinh trong kỳ
    formula: Optional[str] = None  # [35]-[25]
    condition: Optional[str] = None  # ≥ 0, < 0
    dependencies: list = field(default_factory=list)  # ['35', '25']
    data_type: str = "number"


class HTKKFormulaParser:
    """Parse XSD to extract field definitions with formulas."""

    # Indicator pattern: supports both numeric [21] and alphanumeric [A1], [B13], [C3a]
    # - 01/GTGT: [21], [22], [40a]
    # - 03/TNDN: [A1], [B1], [B13], [C3a]
    INDICATOR_PATTERN = r'[A-Za-z]*\d+[a-z]?'

    # Regex patterns for formula extraction
    # More comprehensive patterns to handle TCT's inconsistent formatting
    FORMULA_PATTERNS = [
        # Pattern: ([36]=[35]-[25]) or (B13=A1+B1-B8) - with proper parentheses
        r'\(\[([A-Za-z]*\d+[a-z]?)\]\s*=\s*([^\)]+)\)',
        # Pattern: {[40a]=([36]-[22]+[37]-[38]-[39a]) ≥ 0} - with curly braces
        r'\{\[([A-Za-z]*\d+[a-z]?)\]\s*=\s*([^\}]+)\}',
        # Pattern: ([27]=[29]+[30]+[32]+[32a] - opening paren only (TCT bug)
        r'\(\[([A-Za-z]*\d+[a-z]?)\]\s*=\s*([\[\]\d\w\+\-\*\/\(\)]+)',
        # Pattern: [35]=[28]) or (B13=A1+B1-B8) - closing paren only
        r'\[([A-Za-z]*\d+[a-z]?)\]\s*=\s*([\[\]\d\w\+\-\*\/]+)\)?',
        # Pattern for TNDN: (C4=C1-C2-C3) without brackets in formula
        r'\(([A-Z]\d+[a-z]?)\s*=\s*([A-Z\d\+\-\*\/\(\)]+)\)',
    ]

    # Pattern to extract indicator references like [35], [25], [A1], [B13]
    INDICATOR_REF_PATTERN = r'\[([A-Za-z]*\d+[a-z]?)\]'

    # Condition patterns
    CONDITION_PATTERNS = [
        r'([≥≤<>]=?\s*\d+)',  # ≥ 0, < 0
        r'(nếu\s+.+?\s*[<>≥≤]=?\s*\d+)',  # "nếu ... < 0"
    ]

    def parse_xsd(self, xsd_content: str) -> dict:
        """Parse XSD and extract all fields with formulas."""
        root = ET.fromstring(xsd_content)
        fields = []
        formulas = {}

        # Find CTieuTKhaiChinhType first
        ctieu_type = None
        for ct in root.iter(f"{XS}complexType"):
            if ct.get("name") == "CTieuTKhaiChinhType":
                ctieu_type = ct
                break

        if ctieu_type is None:
            return {"fields": [], "formulas": {}, "dependency_graph": {}}

        # Find all elements within CTieuTKhaiChinhType
        for elem in ctieu_type.iter(f"{XS}element"):
            name = elem.get("name", "")
            if not name or not name.startswith("ct"):
                continue
            # Extract indicator part (ct36 -> 36, ctA1 -> A1, ctB13 -> B13)
            indicator_part = name[2:]
            if not indicator_part:
                continue
            # Must start with digit or uppercase letter (skip appendix elements like ctPL, ctDSTT)
            if not (indicator_part[0].isdigit() or indicator_part[0].isupper()):
                continue
            # Skip list containers (dsXXX, thXXX)
            if name.startswith("ctds") or name.startswith("ctth"):
                continue

            # Get documentation
            doc = self._get_documentation(elem)
            if not doc:
                continue

            # Extract indicator number from element name (ct36 -> 36)
            indicator_num = name[2:]  # Remove "ct" prefix
            indicator = f"[{indicator_num}]"

            # Parse formula from documentation
            formula_info = self._extract_formula(doc, indicator_num)

            field_def = FormulaField(
                element=name,
                indicator=indicator,
                label=self._clean_label(doc),
                formula=formula_info.get("formula"),
                condition=formula_info.get("condition"),
                dependencies=formula_info.get("dependencies", []),
                data_type=self._infer_type(elem),
            )

            fields.append(field_def)

            if field_def.formula:
                formulas[indicator_num] = {
                    "formula": field_def.formula,
                    "dependencies": field_def.dependencies,
                    "condition": field_def.condition,
                }

        return {
            "fields": fields,
            "formulas": formulas,
            "dependency_graph": self._build_dependency_graph(formulas),
        }

    def _get_documentation(self, element) -> str:
        """Extract documentation text from element."""
        annotation = element.find(f"{XS}annotation")
        if annotation is not None:
            doc = annotation.find(f"{XS}documentation")
            if doc is not None and doc.text:
                return doc.text.strip()
        return ""

    def _extract_formula(self, doc: str, target_indicator: str) -> dict:
        """Extract formula, dependencies, and conditions from documentation."""
        result = {"formula": None, "dependencies": [], "condition": None}

        # Escape special regex chars in indicator (for 40a, 32a, etc.)
        escaped_indicator = re.escape(target_indicator)

        # Try each formula pattern
        for pattern in self.FORMULA_PATTERNS:
            matches = re.findall(pattern, doc)
            for match in matches:
                indicator, formula_part = match[0], match[1] if len(match) > 1 else ""
                if indicator == target_indicator:
                    # Found formula for this indicator
                    result["formula"] = self._normalize_formula(formula_part or doc)
                    result["dependencies"] = self._extract_dependencies(result["formula"])
                    break
            if result["formula"]:
                break

        # Try direct pattern matching for this specific indicator
        if not result["formula"]:
            # Pattern: [XX]=[formula with brackets] e.g., [B13]=[A1]+[B1]-[B8]
            direct_pattern = rf'\[{escaped_indicator}\]\s*=\s*([\[\]\d\w\+\-\*\/\(\)]+)'
            direct_match = re.search(direct_pattern, doc)
            if direct_match:
                formula = direct_match.group(1).strip()
                # Make sure it contains at least one indicator reference
                if re.search(r'\[[A-Za-z]*\d+', formula):
                    result["formula"] = self._normalize_formula(formula)
                    result["dependencies"] = self._extract_dependencies(result["formula"])

        # Try pattern without brackets for TNDN: (C4=C1-C2-C3)
        if not result["formula"]:
            # Pattern: (XX=formula) without brackets in formula
            nobracket_pattern = rf'\({escaped_indicator}\s*=\s*([A-Z\d\+\-\*\/\(\)x%]+)\)'
            nobracket_match = re.search(nobracket_pattern, doc, re.IGNORECASE)
            if nobracket_match:
                formula = nobracket_match.group(1).strip()
                # Convert to bracket notation: C1-C2-C3 -> [C1]-[C2]-[C3]
                formula_with_brackets = re.sub(
                    r'([A-Z]\d+[a-z]?)',
                    r'[\1]',
                    formula
                )
                result["formula"] = self._normalize_formula(formula_with_brackets)
                result["dependencies"] = self._extract_dependencies(result["formula"])

        # Extract conditions
        for cond_pattern in self.CONDITION_PATTERNS:
            cond_match = re.search(cond_pattern, doc)
            if cond_match:
                result["condition"] = cond_match.group(1).strip()
                break

        # Special handling for "nếu ... nhỏ hơn 0" or "< 0"
        if "nhỏ hơn 0" in doc or "< 0" in doc:
            result["condition"] = "< 0"
        elif "≥ 0" in doc or ">= 0" in doc:
            result["condition"] = "≥ 0"

        return result

    def _normalize_formula(self, formula: str) -> str:
        """Normalize formula string."""
        # Remove extra whitespace
        formula = re.sub(r'\s+', '', formula)
        # Remove condition suffixes: ≥ 0, < 0, etc.
        formula = re.sub(r'[≥≤<>]=?\s*\d+\s*$', '', formula)
        # Remove trailing unmatched parentheses
        formula = formula.rstrip(')')
        # Remove leading unmatched parentheses
        formula = formula.lstrip('(')
        # Clean up any remaining issues
        formula = formula.strip()

        # Add brackets to indicator references if missing (for TNDN-style formulas)
        # E.g., "B2+B3+B4" -> "[B2]+[B3]+[B4]"
        # But skip if already has brackets
        if not re.search(r'\[', formula) and re.search(r'[A-Z]\d+', formula):
            formula = re.sub(r'([A-Z]\d+[a-z]?)', r'[\1]', formula)

        return formula

    def _extract_dependencies(self, formula: str) -> list:
        """Extract all indicator references from formula."""
        if not formula:
            return []
        matches = re.findall(self.INDICATOR_REF_PATTERN, formula)
        return list(set(matches))  # Unique dependencies

    def _clean_label(self, doc: str) -> str:
        """Remove formula parts from documentation to get clean label."""
        # Remove formula patterns
        label = re.sub(r'\s*\(\[[\d\w]+\]=.+?\)', '', doc)
        label = re.sub(r'\s*\[[\d\w]+\]=.+', '', label)
        label = re.sub(r'\s*\{.+?\}', '', label)
        return label.strip()

    def _infer_type(self, element) -> str:
        """Infer data type from XSD type."""
        xsd_type = element.get("type", "xs:string")
        if "boolean" in xsd_type:
            return "boolean"
        elif any(t in xsd_type for t in ["long", "integer", "int", "decimal"]):
            return "number"
        return "text"

    def _build_dependency_graph(self, formulas: dict) -> dict:
        """Build a dependency graph for calculation order."""
        graph = {}
        for indicator, info in formulas.items():
            graph[indicator] = info.get("dependencies", [])
        return graph

    def get_calculation_order(self, formulas: dict) -> list:
        """Topological sort to get correct calculation order."""
        graph = self._build_dependency_graph(formulas)
        visited = set()
        order = []

        def visit(node):
            if node in visited:
                return
            visited.add(node)
            for dep in graph.get(node, []):
                if dep in graph:  # Only visit if it's a calculated field
                    visit(dep)
            order.append(node)

        for node in graph:
            visit(node)

        return order

    def generate_js_calculator(self, formulas: dict) -> str:
        """Generate JavaScript code for formula calculations."""
        order = self.get_calculation_order(formulas)

        lines = [
            "// Auto-generated from XSD formulas",
            "export function calculateIndicators(data) {",
            "  const result = { ...data };",
            "",
        ]

        for indicator in order:
            info = formulas.get(indicator, {})
            formula = info.get("formula", "")
            condition = info.get("condition", "")

            if not formula:
                continue

            # Convert formula to JS
            js_formula = self._formula_to_js(formula)

            if condition and "≥ 0" in condition:
                lines.append(f"  // [{indicator}] = {formula} (điều kiện: {condition})")
                lines.append(f"  result.ct{indicator} = Math.max(0, {js_formula});")
            elif condition and "< 0" in condition:
                lines.append(f"  // [{indicator}] nếu giá trị < 0")
                lines.append(f"  const temp{indicator} = {js_formula};")
                lines.append(f"  result.ct{indicator} = temp{indicator} < 0 ? Math.abs(temp{indicator}) : 0;")
            else:
                lines.append(f"  // [{indicator}] = {formula}")
                lines.append(f"  result.ct{indicator} = {js_formula};")
            lines.append("")

        lines.append("  return result;")
        lines.append("}")

        return "\n".join(lines)

    def _formula_to_js(self, formula: str) -> str:
        """Convert XSD formula notation to JavaScript."""
        # Replace [XX] or [A1] with result.ctXX or result.ctA1
        js = re.sub(r'\[([A-Za-z]*\d+[a-z]?)\]', r'(result.ct\1 || 0)', formula)
        # Handle percentage notation: x 20% -> * 0.20
        js = re.sub(r'x\s*(\d+)%', r'* 0.\1', js)
        return js


# CLI for testing
if __name__ == "__main__":
    import sys
    import os

    if len(sys.argv) < 2:
        # Default: parse 01_GTGT
        xsd_path = os.path.join(
            os.path.dirname(__file__),
            "schemas/htkk_template/xsd/01_GTGT_TT80_283.xsd"
        )
    else:
        xsd_path = sys.argv[1]

    with open(xsd_path, "r", encoding="utf-8") as f:
        content = f.read()

    parser = HTKKFormulaParser()
    result = parser.parse_xsd(content)

    print("=" * 60)
    print("EXTRACTED FORMULAS")
    print("=" * 60)

    for indicator, info in result["formulas"].items():
        print(f"[{indicator}] = {info['formula']}")
        print(f"  Dependencies: {info['dependencies']}")
        if info.get("condition"):
            print(f"  Condition: {info['condition']}")
        print()

    print("=" * 60)
    print("CALCULATION ORDER")
    print("=" * 60)
    order = parser.get_calculation_order(result["formulas"])
    print(" → ".join(f"[{i}]" for i in order))

    print("\n" + "=" * 60)
    print("GENERATED JAVASCRIPT")
    print("=" * 60)
    print(parser.generate_js_calculator(result["formulas"]))
