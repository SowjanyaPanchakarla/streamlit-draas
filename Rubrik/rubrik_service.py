from rubrik_client import RubrikClient

from queries import (
    PROTECTED_VMS_QUERY,
    LATEST_RECOVERY_POINT_QUERY,
    REPLICATION_FAILURES_QUERY
)

client = RubrikClient()


def get_vm_data():

    result = client.execute_query(
        PROTECTED_VMS_QUERY
    )

    return result["data"]["vSphereVmNewConnection"]["nodes"]


def get_protected_vms():

    vms = get_vm_data()

    output = []

    for vm in vms:

        sla_domain = vm.get(
            "effectiveSlaDomain"
        )

        sla = (
            sla_domain["name"]
            if sla_domain
            else "UNKNOWN"
        )

        if sla not in [
            "UNPROTECTED",
            "DO_NOT_PROTECT"
        ]:

            output.append(
                f"• {vm['name']} ({sla})"
            )

    return "\n".join(output)


def get_protection_summary():

    vms = get_vm_data()

    total = len(vms)

    protected = 0
    unprotected = 0

    for vm in vms:

        sla_domain = vm.get(
            "effectiveSlaDomain"
        )

        sla = (
            sla_domain["name"]
            if sla_domain
            else "UNKNOWN"
        )

        if sla in [
            "UNPROTECTED",
            "DO_NOT_PROTECT"
        ]:

            unprotected += 1

        else:

            protected += 1

    return f"""
### Protection Summary

- Total VMs: {total}
- Protected: {protected}
- Unprotected: {unprotected}
"""


def get_latest_recovery_points():

    result = client.execute_query(
        LATEST_RECOVERY_POINT_QUERY
    )

    vms = result["data"]["vSphereVmNewConnection"]["nodes"]

    output = []

    for vm in vms:

        snapshot = vm.get("newestSnapshot")

        if snapshot is None:

            output.append(
                f"• {vm['name']} : No Recovery Point"
            )

        else:

            output.append(
                f"• {vm['name']} : {snapshot['date']}"
            )

    return "\n".join(output)

def get_vm_recovery_point(vm_name):

    result = client.execute_query(
        LATEST_RECOVERY_POINT_QUERY
    )

    vms = result["data"]["vSphereVmNewConnection"]["nodes"]

    for vm in vms:

        if vm_name.lower() in vm["name"].lower():

            snapshot = vm.get(
                "newestSnapshot"
            )

            if snapshot is None:

                return (
                    f"{vm['name']} "
                    f"has no recovery point."
                )

            return (
                f"### {vm['name']}\n\n"
                f"Latest Recovery Point:\n"
                f"{snapshot['date']}"
            )

    return f"VM '{vm_name}' not found."


def get_replication_failures():

    result = client.execute_query(
        REPLICATION_FAILURES_QUERY
    )

    failures = result["data"]["activitySeriesConnection"]["nodes"]

    if not failures:

        return "No replication failures."

    output = []

    for item in failures:

        output.append(
            f"• {item['objectName']}\n"
            f"  Status: {item['lastActivityStatus']}\n"
            f"  Message: {item['lastActivityMessage']}"
        )

    return "\n\n".join(output)