from apps.clients.models import Client


def get_clients_for_user(user):
    """
    Return queryset of clients accessible to a given user based on role-based permissions.

    Permission Rules:
    ------------------
    1. Super Admin:
        - Has access to ALL clients in the system.

    2. Accountant:
        - Has access only to clients they are assigned to
        - Relationship: Client.accountants (ManyToMany with Account)

    3. Client:
        - Has access only to their own client profile
        - Assumes Client has a direct link to Account (e.g., account/email mapping)

    4. Default (Fallback):
        - No access is granted if role is unrecognized or missing

    Args:
        user (Account): Authenticated user requesting client data.

    Returns:
        QuerySet[Client]: Filtered queryset of accessible clients.
    """

    # Super Admin → everything
    if user.is_superuser:
        return Client.objects.all()

    # Accountant → assigned clients only
    if user.role == user.Role.ACCOUNTANT:
        return Client.objects.filter(accountants=user).distinct()

    # Client → ONLY their own client profile
    if user.role == user.Role.CLIENT:
        return Client.objects.filter(account=user)

    # fallback → NO ACCESS (very important)
    return Client.objects.none()