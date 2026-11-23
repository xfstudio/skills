import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('creation_provenance', Path(__file__).parents[1] / 'scripts/creation_provenance.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CreationProvenanceTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.source = self.save('source.json', [{}, {'A': 'name', 'J': 'code'}])
        self.derived = self.save('derived.json', [{'row': 2, 'A': 'name', 'J': 'code', 'K': None}])
        self.export = self.root / 'catalog.xlsx'
        self.export.write_bytes(b'fixed export bytes')
        self.catalog = self.save('catalog.json', {'source_sha256': module.digest(self.export), 'contracts': {}})

    def save(self, name, value):
        path = self.root / name
        path.write_text(json.dumps(value))
        return path

    def test_hash_representations_require_verified_chain(self):
        source_hashes, catalog_hashes, proof = module.verified_chain(self.source, self.catalog, self.derived, self.export)
        self.assertEqual(source_hashes, {module.digest(self.source), module.digest(self.derived)})
        self.assertEqual(catalog_hashes, {module.digest(self.export), module.digest(self.catalog)})
        self.assertEqual(proof['derived_rows_verified'], 1)
        strict_source, strict_catalog, _ = module.verified_chain(self.source, self.catalog)
        self.assertNotIn(module.digest(self.derived), strict_source)
        self.assertNotIn(module.digest(self.catalog), strict_catalog)

    def test_derived_value_tamper_rejected(self):
        self.save('derived.json', [{'row': 2, 'A': 'other'}])
        with self.assertRaisesRegex(ValueError, 'property differs'):
            module.verified_chain(self.source, self.catalog, self.derived)

    def test_credential_column_and_duplicate_rows_rejected(self):
        for records in [[{'row': 2, 'Z': None}], [{'row': 2}, {'row': 2}]]:
            self.save('derived.json', records)
            with self.assertRaises(ValueError):
                module.verified_chain(self.source, self.catalog, self.derived)

    def test_unrelated_raw_catalog_rejected(self):
        self.export.write_bytes(b'changed export')
        with self.assertRaisesRegex(ValueError, 'Catalog export differs'):
            module.verified_chain(self.source, self.catalog, catalog_export=self.export)

    def test_flat_and_nested_properties_preserve_values(self):
        for record in [{'row': 2, 'J': 'code ', 'K': None}, {'row': 2, 'properties': {'J': 'code ', 'K': None}}]:
            _, rows, normalized = module.property_view({'source_snapshot_sha256': 'fixed', 'rows': [record]})
            self.assertEqual(rows, [2])
            self.assertEqual(normalized[0]['properties'], {'J': 'code ', 'K': None})
        with self.assertRaisesRegex(ValueError, 'credential'):
            module.property_view({'rows': [{'row': 2, 'AA': None}]})

    def test_non_executable_references_not_promoted(self):
        plan = {'execution_bindings_exact': True, 'execution_bindings': {'live': {'code': 'live', 'version': '1'}},
                'not_bound_contracts': [{'code': 'blocked', 'version': '1'}], 'executable_atp_codes': ['live']}
        bindings, _ = module.execution_view(plan)
        self.assertEqual(bindings, [{'code': 'live', 'version': '1'}])
        plan['executable_atp_codes'].append('blocked')
        with self.assertRaisesRegex(ValueError, 'allowlist differs'):
            module.execution_view(plan)

    def test_nested_ordered_execution_bindings_checked(self):
        plan = {'execution_bindings_exact': True, 'ordered_execution_plan': [
            {'ordered_steps': [{'code': 'live', 'version': '1'}, {'mechanism': 'native'}]}]}
        self.assertEqual(module.execution_view(plan)[0], [{'code': 'live', 'version': '1'}])
        plan['execution_bindings_exact'] = False
        with self.assertRaises(ValueError):
            module.execution_view(plan)


if __name__ == '__main__':
    unittest.main()
