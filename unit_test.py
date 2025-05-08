import unittest
from parser import parse_hl7_message  # type: ignore
import textwrap

class UnitTest(unittest.TestCase):

    def test_valid_message(self):
        hl7_message = textwrap.dedent("""\
            MSH|^~\\&|EMR|HOSPITAL|RCM|RCMSYSTEM|202505021200||SIU^S12|12345|P|2.3
            SCH|123456^A|...|202505021300|...|Clinic A - Room 203|...
            PID|1||P12345^^^HOSP^MR||Doe^John||19850210|M
            PV1|1|...|D67890^Smith^Dr
        """)
        
        result = parse_hl7_message(hl7_message)
        self.assertEqual(result["appointment_id"], "123456")
        self.assertEqual(result["appointment_datetime"], "2025-05-02T13:00:00Z")
        self.assertEqual(result["patient"]["id"], "P12345")
        self.assertEqual(result["patient"]["first_name"], "John")
        self.assertEqual(result["patient"]["last_name"], "Doe")
        self.assertEqual(result["patient"]["dob"], "1985-02-10")
        self.assertEqual(result["patient"]["gender"], "M")
        self.assertEqual(result["provider"]["id"], "D67890")
        self.assertEqual(result["provider"]["name"], "Dr. Smith")
        self.assertEqual(result["location"], "Clinic A - Room 203")
        self.assertEqual(result["reason"], "...")

    
    def test_malformed_datetime(self):
        hl7 = textwrap.dedent("""\
            MSH|^~\\&|EMR|HOSPITAL|RCM|RCMSYSTEM|202505021200||SIU^S12|12345|P|2.3
            SCH|123456^A|General Consultation|2025/05-02 13:00|...|Clinic A - Room 203
            PID|1||P12345^^^HOSP^MR||Doe^John||19850210|M
            PV1|1|...|D67890^Smith^Dr
        """)

        result = parse_hl7_message(hl7)
        self.assertIsNone(result)


    def test_empty_required_fields(self):
            hl7 = textwrap.dedent("""\
            MSH|^~\\&|EMR|HOSPITAL|RCM|RCMSYSTEM|202505021200||SIU^S12|12345|P|2.3
            SCH|123456^A||202505021300|...|Clinic A - Room 203
            PID|1||P12345^^^HOSP^MR||Doe^John||19850210|
            PV1|1|...|D67890^Smith^Dr
        """)

            result = parse_hl7_message(hl7)
            self.assertIsNone(result)

            



if __name__ == '__main__':
    unittest.main()