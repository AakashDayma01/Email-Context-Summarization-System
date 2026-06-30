from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.accounts.models import Account
from apps.clients.models import Client
from apps.emails.models import Email
from apps.firms.models import Firm


class Command(BaseCommand):
    help = "Seed mock Email Context Summarization data"

    def handle(self, *args, **kwargs):

        self.stdout.write(self.style.SUCCESS("Creating Firms..."))

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
                        f"Created Firm: {firm.name}"
                    )
                )

        #######################################################
        # USERS
        #######################################################
        users = [

            ###################################################
            # SUPER ADMINS
            ###################################################

            {
                "username": "ascend_admin",
                "email": "admin@ascend.com",
                "password": "Admin@123",
                "firm": "Ascend CPA",
                "first_name": "Rahul",
                "last_name": "Sharma",
                "is_superuser": True,
                "is_staff": True,
            },

            {
                "username": "elite_admin",
                "email": "admin@elite.com",
                "password": "Admin@123",
                "firm": "Elite Tax Consultants",
                "first_name": "Priya",
                "last_name": "Patel",
                "is_superuser": True,
                "is_staff": True,
            },

            ###################################################
            # ACCOUNTANTS
            ###################################################

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
                "username": "alice",
                "email": "alice@elite.com",
                "password": "Accountant@123",
                "role": Account.Role.ACCOUNTANT,
                "firm": "Elite Tax Consultants",
                "first_name": "Alice",
                "last_name": "Johnson",
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

            ###################################################
            # CLIENT LOGIN ACCOUNTS
            ###################################################

            {
                "username": "abc_client",
                "email": "contact@abcpvt.com",
                "password": "Client@123",
                "role": Account.Role.CLIENT,
                "firm": "Ascend CPA",
                "first_name": "ABC",
                "last_name": "Pvt Ltd",
            },

            {
                "username": "xyz_client",
                "email": "info@xyztech.com",
                "password": "Client@123",
                "role": Account.Role.CLIENT,
                "firm": "Ascend CPA",
                "first_name": "XYZ",
                "last_name": "Technologies",
            },

            {
                "username": "bright_client",
                "email": "admin@brightsolutions.com",
                "password": "Client@123",
                "role": Account.Role.CLIENT,
                "firm": "Elite Tax Consultants",
                "first_name": "Bright",
                "last_name": "Solutions",
            },

            {
                "username": "green_client",
                "email": "contact@greenenterprises.com",
                "password": "Client@123",
                "role": Account.Role.CLIENT,
                "firm": "Elite Tax Consultants",
                "first_name": "Green",
                "last_name": "Enterprises",
            },
        ]

        self.stdout.write(self.style.SUCCESS("Creating Users..."))

        for user_data in users:

            firm = Firm.objects.get(name=user_data["firm"])

            user, created = Account.objects.get_or_create(
                email=user_data["email"],
                defaults={
                    "username": user_data["username"],
                    "first_name": user_data["first_name"],
                    "last_name": user_data["last_name"],
                    "firm": firm,
                    "role": user_data.get("role", Account.Role.ACCOUNTANT),
                    "is_superuser": user_data.get("is_superuser", False),
                    "is_staff": user_data.get("is_staff", False),
                },
            )

            if created:
                user.set_password(user_data["password"])
                user.save()

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created User: {user.email}"
                    )
                )

            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"User already exists: {user.email}"
                    )
                )
        #######################################################
        # CLIENT CREATION
        #######################################################

        clients = [

            {
                "firm": "Ascend CPA",
                "name": "ABC Pvt Ltd",
                "email": "contact@abcpvt.com",
                "phone": "9876543210",
                "account": "contact@abcpvt.com",
                "accountants": [
                    "john@ascend.com",
                    "ca.rohit@ascend.com",
                    "ca.neha@ascend.com",
                ],
            },

            {
                "firm": "Ascend CPA",
                "name": "XYZ Technologies",
                "email": "info@xyztech.com",
                "phone": "9876543211",
                "account": "info@xyztech.com",
                "accountants": [
                    "john@ascend.com",
                    "ca.rohit@ascend.com",
                ],
            },

            {
                "firm": "Elite Tax Consultants",
                "name": "Bright Solutions",
                "email": "admin@brightsolutions.com",
                "phone": "9876543212",
                "account": "admin@brightsolutions.com",
                "accountants": [
                    "alice@elite.com",
                    "ca.karan@elite.com",
                ],
            },

            {
                "firm": "Elite Tax Consultants",
                "name": "Green Enterprises",
                "email": "contact@greenenterprises.com",
                "phone": "9876543213",
                "account": "contact@greenenterprises.com",
                "accountants": [
                    "alice@elite.com",
                    "ca.karan@elite.com",
                ],
            },

        ]

        self.stdout.write(self.style.SUCCESS("Creating Clients..."))

        for client_data in clients:

            firm = Firm.objects.get(
                name=client_data["firm"]
            )

            account = Account.objects.get(
                email=client_data["account"]
            )

            client, created = Client.objects.get_or_create(

                email=client_data["email"],

                defaults={

                    "firm": firm,
                    "account": account,
                    "name": client_data["name"],
                    "phone": client_data["phone"],

                },

            )

            # Assign accountants
            for accountant_email in client_data["accountants"]:

                accountant = Account.objects.get(
                    email=accountant_email
                )

                client.accountants.add(accountant)

            if created:

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created Client: {client.name}"
                    )
                )

            else:

                self.stdout.write(
                    self.style.WARNING(
                        f"Client already exists: {client.name}"
                    )
                )
        #######################################################
        # EMAIL SEEDING
        #######################################################

        emails = [

            # ===========================================
            # ABC Pvt Ltd
            # ===========================================

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
                "body": "We are still waiting for your Form-16.",
            },

            {
                "client": "ABC Pvt Ltd",
                "accountant": "ca.neha@ascend.com",
                "subject": "Investment Proof",
                "body": "Please upload your investment proofs.",
            },

            {
                "client": "ABC Pvt Ltd",
                "accountant": "admin@ascend.com",
                "subject": "Acknowledgement",
                "body": "We have received your documents.",
            },

            # ===========================================
            # XYZ Technologies
            # ===========================================

            {
                "client": "XYZ Technologies",
                "accountant": "john@ascend.com",
                "subject": "GST Return",
                "body": "Please upload GST return.",
            },

            {
                "client": "XYZ Technologies",
                "accountant": "ca.rohit@ascend.com",
                "subject": "Purchase Register",
                "body": "Kindly upload purchase register.",
            },

            {
                "client": "XYZ Technologies",
                "accountant": "admin@ascend.com",
                "subject": "Reminder",
                "body": "GST documents are pending.",
            },

            # ===========================================
            # Bright Solutions
            # ===========================================

            {
                "client": "Bright Solutions",
                "accountant": "alice@elite.com",
                "subject": "Salary Slips",
                "body": "Please upload salary slips.",
            },

            {
                "client": "Bright Solutions",
                "accountant": "ca.karan@elite.com",
                "subject": "PAN Card",
                "body": "Please upload PAN cards.",
            },

            {
                "client": "Bright Solutions",
                "accountant": "admin@elite.com",
                "subject": "Acknowledgement",
                "body": "Documents received.",
            },

            # ===========================================
            # Green Enterprises
            # ===========================================

            {
                "client": "Green Enterprises",
                "accountant": "alice@elite.com",
                "subject": "ITR Documents",
                "body": "Please upload ITR documents.",
            },

            {
                "client": "Green Enterprises",
                "accountant": "ca.karan@elite.com",
                "subject": "Reminder",
                "body": "ITR documents pending.",
            },

            {
                "client": "Green Enterprises",
                "accountant": "admin@elite.com",
                "subject": "Verification",
                "body": "Verification is in progress.",
            },

        ]

        self.stdout.write(
            self.style.SUCCESS("Creating Emails...")
        )

        for index, email_data in enumerate(emails):

            client = Client.objects.get(
                name=email_data["client"]
            )

            accountant = Account.objects.get(
                email=email_data["accountant"]
            )

            email, created = Email.objects.get_or_create(

                client=client,
                accountant=accountant,
                subject=email_data["subject"],

                defaults={
                    "body": email_data["body"],
                }

            )

            if created:

                # Preserve chronological ordering
                email.sent_at = timezone.now() - timedelta(days=index)
                email.save(update_fields=["sent_at"])

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created Email : {email.subject}"
                    )
                )

            else:

                self.stdout.write(
                    self.style.WARNING(
                        f"Email already exists : {email.subject}"
                    )
                )

        #######################################################
        # FINISHED
        #######################################################

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("=" * 60))
        self.stdout.write(self.style.SUCCESS("DATABASE SEEDED SUCCESSFULLY"))
        self.stdout.write(self.style.SUCCESS("=" * 60))