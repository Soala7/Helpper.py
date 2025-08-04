import requests
import json
import re
import time
from urllib.parse import quote

class ChemicalStructureAPI:
    def __init__(self):
        self.pubchem_base = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
        self.chemspider_base = "https://www.chemspider.com/Chemical-Structure"
        
    def get_compound_from_pubchem(self, formula):
        """Get compound data from PubChem API using molecular formula"""
        try:
            # Search by molecular formula
            url = f"{self.pubchem_base}/compound/formula/{formula}/JSON"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'PC_Compounds' in data:
                    return data['PC_Compounds'][0]
            return None
        except Exception as e:
            print(f"PubChem API error: {e}")
            return None
    
    def get_compound_properties(self, cid):
        """Get additional properties using compound ID"""
        try:
            properties = [
                'MolecularFormula', 'MolecularWeight', 'IUPACName', 
                'CanonicalSMILES', 'InChI', 'XLogP', 'TPSA'
            ]
            prop_string = ','.join(properties)
            url = f"{self.pubchem_base}/compound/cid/{cid}/property/{prop_string}/JSON"
            
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data['PropertyTable']['Properties'][0]
            return None
        except Exception as e:
            print(f"Properties API error: {e}")
            return None
    
    def get_structure_image_url(self, cid, size='large'):
        """Get 2D structure image URL from PubChem"""
        return f"{self.pubchem_base}/compound/cid/{cid}/PNG?image_size={size}"
    
    def smiles_to_structure(self, smiles):
        """Convert SMILES to ASCII structure representation"""
        structure_map = {
            # Single bonds
            'C-C': 'C-C',
            'C-H': 'C-H',
            # Double bonds  
            'C=C': 'C=C',
            'C=O': 'C=O',
            # Triple bonds
            'C#C': 'C≡C',
            'C#N': 'C≡N',
            # Rings
            'c': 'C', # aromatic carbon
            # Branches
            '(': '(',
            ')': ')',
        }
        
        # Simple SMILES parsing for basic structures
        ascii_structure = smiles
        for smiles_notation, ascii_notation in structure_map.items():
            ascii_structure = ascii_structure.replace(smiles_notation, ascii_notation)
        
        return ascii_structure

class OrganicCompoundAnalyzer:
    def __init__(self):
        self.api = ChemicalStructureAPI()
        
    def analyze_compound(self, formula):
        """Comprehensive compound analysis using APIs"""
        print(f"\n{'='*50}")
        print(f"ANALYZING: {formula}")
        print(f"{'='*50}")
        
        # Get basic compound data
        compound_data = self.api.get_compound_from_pubchem(formula)
        
        if not compound_data:
            print("❌ Compound not found in PubChem database")
            print("Falling back to basic structure generation...")
            self._fallback_analysis(formula)
            return
        
        # Extract CID (Compound ID)
        cid = compound_data['id']['id']['cid']
        print(f"✅ Found in PubChem! CID: {cid}")
        
        # Get detailed properties
        properties = self.api.get_compound_properties(cid)
        
        if properties:
            self._display_compound_info(properties, cid)
            self._generate_structure_from_smiles(properties.get('CanonicalSMILES'))
        
        # Provide image URL for detailed structure
        image_url = self.api.get_structure_image_url(cid)
        print(f"\n🖼️  Detailed 2D Structure Image:")
        print(f"📎 {image_url}")
        
    def _display_compound_info(self, properties, cid):
        """Display comprehensive compound information"""
        print(f"\n📋 COMPOUND INFORMATION:")
        print(f"├─ Molecular Formula: {properties.get('MolecularFormula', 'N/A')}")
        print(f"├─ Molecular Weight: {properties.get('MolecularWeight', 'N/A')} g/mol")
        print(f"├─ IUPAC Name: {properties.get('IUPACName', 'N/A')}")
        print(f"├─ SMILES: {properties.get('CanonicalSMILES', 'N/A')}")
        print(f"├─ XLogP: {properties.get('XLogP', 'N/A')} (lipophilicity)")
        print(f"└─ TPSA: {properties.get('TPSA', 'N/A')} Ų (polar surface area)")
        
    def _generate_structure_from_smiles(self, smiles):
        """Generate ASCII structure from SMILES notation"""
        if not smiles:
            return
            
        print(f"\n🧪 MOLECULAR STRUCTURE:")
        print(f"SMILES: {smiles}")
        
        # Enhanced structure generation based on SMILES
        structure_lines = self._advanced_smiles_to_ascii(smiles)
        
        print("ASCII Structure:")
        print("┌" + "─" * (max(len(line) for line in structure_lines) + 2) + "┐")
        for line in structure_lines:
            print(f"│ {line:<{max(len(l) for l in structure_lines)}} │")
        print("└" + "─" * (max(len(line) for line in structure_lines) + 2) + "┘")
        
    def _advanced_smiles_to_ascii(self, smiles):
        """Advanced SMILES to ASCII conversion"""
        # Detect bond types and create appropriate representations
        structure = []
        
        if '≡' in smiles or '#' in smiles:
            # Triple bond compounds (alkynes)
            if 'C#C' in smiles:
                structure = [
                    "R-C≡C-R'",
                    "  │   │  ",
                    "  H   H  "
                ]
        elif '=' in smiles:
            # Double bond compounds (alkenes, carbonyls)
            if 'C=C' in smiles:
                structure = [
                    "R   R'",
                    " \\ / ",
                    "  C=C ",
                    " / \\ ",
                    "H   H"
                ]
            elif 'C=O' in smiles:
                structure = [
                    "    O",
                    "    ‖",
                    "R-C-R'",
                    "  │   ",
                    "  H   "
                ]
        else:
            # Single bond compounds (alkanes)
            carbon_count = smiles.count('C')
            if carbon_count == 1:
                structure = [
                    "  H  ",
                    "  │  ",
                    "H-C-H",
                    "  │  ",
                    "  H  "
                ]
            elif carbon_count == 2:
                structure = [
                    "H   H",
                    "│   │",
                    "H-C-C-H",
                    "│   │",
                    "H   H"
                ]
            else:
                # Linear chain representation
                chain = "H-" + "-".join(['C'] * carbon_count) + "-H"
                structure = [chain]
        
        return structure if structure else [f"Structure: {smiles}"]
    
    def _fallback_analysis(self, formula):
        """Fallback analysis when API fails"""
        print("\n🔄 Using offline analysis...")
        
        # Extract atoms
        carbon_match = re.search(r'C(\d*)', formula)
        hydrogen_match = re.search(r'H(\d*)', formula)
        
        carbon_count = 1 if carbon_match and carbon_match.group(1) == '' else int(carbon_match.group(1)) if carbon_match else 0
        hydrogen_count = 1 if hydrogen_match and hydrogen_match.group(1) == '' else int(hydrogen_match.group(1)) if hydrogen_match else 0
        
        print(f"📊 Basic Analysis:")
        print(f"├─ Carbon atoms: {carbon_count}")
        print(f"├─ Hydrogen atoms: {hydrogen_count}")
        
        # Determine compound type
        if carbon_count > 0:
            expected_alkane = 2 * carbon_count + 2
            expected_alkene = 2 * carbon_count
            expected_alkyne = 2 * carbon_count - 2
            
            if hydrogen_count == expected_alkane:
                compound_type = "Alkane (single bonds)"
                bond_symbol = "-"
            elif hydrogen_count == expected_alkene:
                compound_type = "Alkene (double bond)"
                bond_symbol = "="
            elif hydrogen_count == expected_alkyne:
                compound_type = "Alkyne (triple bond)"
                bond_symbol = "≡"
            else:
                compound_type = "Unknown/Complex compound"
                bond_symbol = "-"
            
            print(f"└─ Compound type: {compound_type}")
            
            # Generate basic structure
            self._generate_basic_structure(carbon_count, bond_symbol)
    
    def _generate_basic_structure(self, carbon_count, bond_symbol):
        """Generate basic structure representation"""
        print(f"\n🏗️  BASIC STRUCTURE:")
        
        if carbon_count == 1:
            structure = [
                "  H  ",
                "  │  ",
                "H-C-H",
                "  │  ",
                "  H  "
            ]
        elif carbon_count == 2:
            if bond_symbol == "≡":
                structure = ["H-C≡C-H"]
            elif bond_symbol == "=":
                structure = [
                    "H   H",
                    " \\ /",
                    "  C=C",
                    " / \\",
                    "H   H"
                ]
            else:
                structure = [
                    "H   H",
                    "│   │",
                    "H-C-C-H",
                    "│   │",
                    "H   H"
                ]
        else:
            # Linear representation for larger molecules
            atoms = ['C'] * carbon_count
            chain = f"H-{bond_symbol.join(atoms)}-H"
            structure = [chain]
        
        for line in structure:
            print(f"    {line}")

def main():
    """Main program with API integration"""
    analyzer = OrganicCompoundAnalyzer()
    
    print("🧬 ADVANCED CHEMICAL STRUCTURE ANALYZER")
    print("💡 Powered by PubChem API for unlimited compound data!")
    print("📝 Enter formulas like: CH4, C2H4, C2H2, C6H6, etc.")
    print("⚠️  Note: Requires internet connection for full features")
    print("\nType 'quit' to exit, 'help' for examples")
    
    example_compounds = [
        "CH4", "C2H6", "C3H8", "C4H10",  # Alkanes
        "C2H4", "C3H6", "C4H8",           # Alkenes  
        "C2H2", "C3H4",                   # Alkynes
        "C6H6", "C7H8",                   # Aromatics
        "CH3OH", "C2H5OH",                # Alcohols
        "CH2O", "C2H4O"                   # Carbonyls
    ]
    
    while True:
        formula = input(f"\n{'='*20}\nEnter formula: ").strip()
        
        if formula.lower() == 'quit':
            print("👋 Thanks for using the Chemical Structure Analyzer!")
            break
        elif formula.lower() == 'help':
            print(f"\n📚 Example compounds to try:")
            for i, compound in enumerate(example_compounds, 1):
                print(f"{i:2d}. {compound}")
            continue
        elif not formula:
            print("❌ Please enter a valid chemical formula")
            continue
        
        try:
            # Clean up the formula
            clean_formula = ''.join([char.upper() if char.isalpha() else char for char in formula])
            analyzer.analyze_compound(clean_formula)
            
        except KeyboardInterrupt:
            print("\n⏹️  Operation cancelled by user")
            continue
        except Exception as e:
            print(f"❌ Error analyzing compound: {e}")
            print("🔄 Try again with a different formula")

if __name__ == "__main__":
    main()