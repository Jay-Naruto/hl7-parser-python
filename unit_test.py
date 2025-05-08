import unittest
from parser import parse_hl7_message  # type: ignore
from main import split_messages  # type: ignore

class UnitTest(unittest.TestCase):

    def testParser(self):
        hl7_message = """
                        MSH|^~\\&|EMR|HOSPITAL|RCM|RCMSYSTEM|202505021200||SIU^S12|12345|P|2.3
                        SCH|123456^A|...|202505021300|...|Clinic A - Room 203|...
                        PID|1||P12345^^^HOSP^MR||Doe^John||19850210|M
                        PV1|1|...|D67890^Smith^Dr

                     """
        result = [parse_hl7_message(msg) for msg in split_messages(hl7_message)]
        self.assertEqual(result[0]["appointment_id"], "123456")
        self.assertEqual(result[0]["appointment_datetime"], "2025-05-02T13:00:00Z")
        self.assertEqual(result[0]["patient"]["id"], "P12345")
        self.assertEqual(result[0]["patient"]["first_name"], "John")
        self.assertEqual(result[0]["patient"]["last_name"], "Doe")
        self.assertEqual(result[0]["patient"]["dob"], "1985-02-10")
        self.assertEqual(result[0]["patient"]["gender"], "M")
        self.assertEqual(result[0]["provider"]["id"], "D67890")
        self.assertEqual(result[0]["provider"]["name"], "Dr. Smith")
        self.assertEqual(result[0]["location"], "Clinic A - Room 203")
        self.assertEqual(result[0]["reason"], "...")

if __name__ == '__main__':
    unittest.main()