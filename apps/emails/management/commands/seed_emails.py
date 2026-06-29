from django.core.management.base import BaseCommand
from apps.firms.models import Firm
from apps.accounts.models import Account
from apps.clients.models import Client
from apps.emails.models import Email
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = "Seed mock email data"

    def handle(self, *args, **kwargs):

        firms = [
            "Ascend CPA",
            "Elite Tax Consultants",
        ]

        for firm_name in firms:
            firm, created = Firm.objects.get_or_create(
                name=firm_name
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Firm created: {firm.name}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Firm already exists: {firm.name}"
                    )
                )
        users = [
            {
                "username": "ascend_admin",
                "email": "admin@ascend.com",
                "password": "Admin@123",
                "role": Account.Role.ADMIN,
                "firm": "Ascend CPA",
                "first_name": "Rahul",
                "last_name": "Sharma",
            },
            {
                "username": "john",
                "email": "john@ascend.com",
                "password": "Accountant@123",
                "role": Account.Role.ACCOUNTANT,
                "firm": "Ascend CPA",
                "first_name": "John",
                "last_name": "Doe",
            },
            {
                "username": "elite_admin",
                "email": "admin@elite.com",
                "password": "Admin@123",
                "role": Account.Role.ADMIN,
                "firm": "Elite Tax Consultants",
                "first_name": "Priya",
                "last_name": "Patel",
            },
            {
                "username": "alice",
                "email": "alice@elite.com",
                "password": "Accountant@123",
                "role": Account.Role.ACCOUNTANT,
                "firm": "Elite Tax Consultants",
                "first_name": "Alice",
                "last_name": "Johnson",
            },
            {
                "username": "rohit",
                "email": "ca.rohit@ascend.com",
                "password": "Accountant@123",
                "role": Account.Role.ACCOUNTANT,
                "firm": "Ascend CPA",
                "first_name": "Rohit",
                "last_name": "Gupta",
            },
            {
                "username": "neha",
                "email": "ca.neha@ascend.com",
                "password": "Accountant@123",
                "role": Account.Role.ACCOUNTANT,
                "firm": "Ascend CPA",
                "first_name": "Neha",
                "last_name": "Verma",
            },
            {
                "username": "karan",
                "email": "ca.karan@elite.com",
                "password": "Accountant@123",
                "role": Account.Role.ACCOUNTANT,
                "firm": "Elite Tax Consultants",
                "first_name": "Karan",
                "last_name": "Singh",
            },
        ]

        for user_data in users:

            firm = Firm.objects.get(name=user_data["firm"])

            user, created = Account.objects.get_or_create(
                email=user_data["email"],
                defaults={
                    "username": user_data["username"],
                    "first_name": user_data["first_name"],
                    "last_name": user_data["last_name"],
                    "role": user_data["role"],
                    "firm": firm,
                },
            )

            if created:
                user.set_password(user_data["password"])
                user.save()

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created user: {user.email}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"User already exists: {user.email}"
                    )
                )

        clients = [
            {
                "firm": "Ascend CPA",
                "name": "ABC Pvt Ltd",
                "email": "contact@abcpvt.com",
                "phone": "9876543210",
            },
            {
                "firm": "Ascend CPA",
                "name": "XYZ Technologies",
                "email": "info@xyztech.com",
                "phone": "9876543211",
            },
            {
                "firm": "Elite Tax Consultants",
                "name": "Bright Solutions",
                "email": "admin@brightsolutions.com",
                "phone": "9876543212",
            },
            {
                "firm": "Elite Tax Consultants",
                "name": "Green Enterprises",
                "email": "contact@greenenterprises.com",
                "phone": "9876543213",
            },
        ]

        for client_data in clients:

            firm = Firm.objects.get(name=client_data["firm"])

            client, created = Client.objects.get_or_create(
                email=client_data["email"],
                defaults={
                    "firm": firm,
                    "name": client_data["name"],
                    "phone": client_data["phone"],
                },
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created client: {client.name}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Client already exists: {client.name}"
                    )
                )

        emails = [
            {
                "client": "ABC Pvt Ltd",
                "accountant": "john@ascend.com",
                "subject": "Request for Form-16",
                "body": "Please upload your Form-16 for FY 2025-26.",
            },
            {
                "client": "ABC Pvt Ltd",
                "accountant": "admin@ascend.com",
                "subject": "Bank Statements",
                "body": "Kindly share your bank statements from April to March.",
            },
            {
                "client": "ABC Pvt Ltd",
                "accountant": "john@ascend.com",
                "subject": "Investment Proof",
                "body": "We are still waiting for your investment proof documents.",
            },
            {
                "client": "XYZ Technologies",
                "accountant": "john@ascend.com",
                "subject": "GST Documents",
                "body": "Please send the GST returns for the last quarter.",
            },
            {
                "client": "XYZ Technologies",
                "accountant": "admin@ascend.com",
                "subject": "Acknowledgement",
                "body": "Thank you for sharing the GST documents.",
            },
            {
                "client": "Bright Solutions",
                "accountant": "alice@elite.com",
                "subject": "Salary Slips",
                "body": "Please upload salary slips for all directors.",
            },
            {
                "client": "Bright Solutions",
                "accountant": "admin@elite.com",
                "subject": "Reminder",
                "body": "This is a reminder to submit pending salary slips.",
            },
            {
                "client": "Green Enterprises",
                "accountant": "alice@elite.com",
                "subject": "ITR Documents",
                "body": "Please upload all documents required for ITR filing.",
            },
            {
                "client": "Green Enterprises",
                "accountant": "admin@elite.com",
                "subject": "Verification",
                "body": "We have received your documents. Verification is in progress.",
            },
            {
                "client": "ABC Pvt Ltd",
                "accountant": "john@ascend.com",
                "subject": "Request for Form-16",
                "body": "Please upload your Form-16 for FY 2025-26.",
            },
            {
                "client": "ABC Pvt Ltd",
                "accountant": "ca.rohit@ascend.com",
                "subject": "Reminder - Form-16",
                "body": "We are still waiting for your Form-16 documents.",
            },
            {
                "client": "ABC Pvt Ltd",
                "accountant": "admin@ascend.com",
                "subject": "Bank Statements",
                "body": "Please upload bank statements from April to March.",
            },
            {
                "client": "ABC Pvt Ltd",
                "accountant": "john@ascend.com",
                "subject": "Reminder - Bank Statements",
                "body": "Kindly share bank statements again.",
            },
            {
                "client": "ABC Pvt Ltd",
                "accountant": "ca.neha@ascend.com",
                "subject": "Investment Proof",
                "body": "Please upload investment proof under section 80C.",
            },
            {
                "client": "ABC Pvt Ltd",
                "accountant": "john@ascend.com",
                "subject": "Investment Proof Reminder",
                "body": "Reminder for pending investment proof documents.",
            },
            {
                "client": "ABC Pvt Ltd",
                "accountant": "admin@ascend.com",
                "subject": "Acknowledgement",
                "body": "Thank you. We have received your Form-16.",
            },



            # ---------------- XYZ Technologies ----------------

            {
                "client": "XYZ Technologies",
                "accountant": "john@ascend.com",
                "subject": "GST Returns",
                "body": "Please send GST returns for the last quarter.",
            },
            {
                "client": "XYZ Technologies",
                "accountant": "ca.rohit@ascend.com",
                "subject": "GST Reminder",
                "body": "Reminder to upload GST returns.",
            },
            {
                "client": "XYZ Technologies",
                "accountant": "ca.neha@ascend.com",
                "subject": "GST Reminder Again",
                "body": "We have not received GST documents yet.",
            },
            {
                "client": "XYZ Technologies",
                "accountant": "admin@ascend.com",
                "subject": "Purchase Register",
                "body": "Please upload purchase register.",
            },
            {
                "client": "XYZ Technologies",
                "accountant": "john@ascend.com",
                "subject": "Purchase Register Reminder",
                "body": "Kindly upload purchase register.",
            },
            {
                "client": "XYZ Technologies",
                "accountant": "admin@ascend.com",
                "subject": "Acknowledgement",
                "body": "Thank you. GST documents received.",
            },



            # ---------------- Bright Solutions ----------------

            {
                "client": "Bright Solutions",
                "accountant": "alice@elite.com",
                "subject": "Salary Slips",
                "body": "Please upload salary slips for all directors.",
            },
            {
                "client": "Bright Solutions",
                "accountant": "ca.karan@elite.com",
                "subject": "Reminder Salary Slips",
                "body": "Salary slips are still pending.",
            },
            {
                "client": "Bright Solutions",
                "accountant": "admin@elite.com",
                "subject": "Director PAN",
                "body": "Please upload PAN cards of directors.",
            },
            {
                "client": "Bright Solutions",
                "accountant": "alice@elite.com",
                "subject": "PAN Reminder",
                "body": "Reminder to upload PAN cards.",
            },
            {
                "client": "Bright Solutions",
                "accountant": "admin@elite.com",
                "subject": "Acknowledgement",
                "body": "Documents received successfully.",
            },



            # ---------------- Green Enterprises ----------------

            {
                "client": "Green Enterprises",
                "accountant": "alice@elite.com",
                "subject": "ITR Documents",
                "body": "Please upload documents for ITR filing.",
            },
            {
                "client": "Green Enterprises",
                "accountant": "ca.karan@elite.com",
                "subject": "Reminder ITR Documents",
                "body": "ITR documents are pending.",
            },
            {
                "client": "Green Enterprises",
                "accountant": "admin@elite.com",
                "subject": "Bank Statements",
                "body": "Please upload latest bank statements.",
            },
            {
                "client": "Green Enterprises",
                "accountant": "alice@elite.com",
                "subject": "Reminder Bank Statements",
                "body": "Waiting for bank statements.",
            },
            {
                "client": "Green Enterprises",
                "accountant": "admin@elite.com",
                "subject": "Verification",
                "body": "We have received all documents. Verification in progress.",
            },


        ]

        for index, email_data in enumerate(emails):
            client = Client.objects.get(name=email_data["client"])

            accountant = Account.objects.get(email=email_data["accountant"])

            email, created = Email.objects.get_or_create(
                client=client,
                accountant=accountant,
                subject=email_data["subject"],
                defaults={
                    "body": email_data["body"],
                    "sent_at": timezone.now() - timedelta(days=len(emails) - index),
                },
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Email created: {email.subject}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Email already exists: {email.subject}"
                    )
                )
        self.stdout.write(
            self.style.SUCCESS("Firm seeding completed.")
        )