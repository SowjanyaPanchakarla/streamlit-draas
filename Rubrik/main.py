from rubrik_client import RubrikClient
from queries import PROTECTED_VMS_QUERY , LATEST_RECOVERY_POINT_QUERY

CLIENT_ID = "client|2adb81cb-f913-4234-98c0-0ba6d22bb6be"
CLIENT_SECRET = "8LWZCFTofA5CL-14CLQ2W9VT-e9U7wf3eTHoVTP9grtDl78Q0kM8m1IZJ9lZFVxG"

client = RubrikClient(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)


def get_protected_vms():

    result = client.execute_query(PROTECTED_VMS_QUERY)

    vms = result["data"]["vSphereVmNewConnection"]["nodes"]

    print("\nProtected VMs")
    print("-" * 50)

    for vm in vms:

        sla = vm["effectiveSlaDomain"]["name"]

        if sla not in ["UNPROTECTED", "DO_NOT_PROTECT"]:

            print(f"{vm['name']} - {sla}")


def check_vm_protection(vm_name):

    result = client.execute_query(PROTECTED_VMS_QUERY)

    vms = result["data"]["vSphereVmNewConnection"]["nodes"]

    for vm in vms:

        if vm["name"].lower() == vm_name.lower():

            sla = vm["effectiveSlaDomain"]["name"]

            if sla in ["UNPROTECTED", "DO_NOT_PROTECT"]:

                return f"{vm_name} is not protected."

            return f"{vm_name} is protected under SLA '{sla}'."

    return f"{vm_name} not found."


def get_unprotected_vms():

    result = client.execute_query(PROTECTED_VMS_QUERY)

    vms = result["data"]["vSphereVmNewConnection"]["nodes"]

    print("\nUnprotected VMs")
    print("-" * 50)

    for vm in vms:

        sla = vm["effectiveSlaDomain"]["name"]

        if sla in ["UNPROTECTED", "DO_NOT_PROTECT"]:

            print(f"{vm['name']} - {sla}")


def get_protection_summary():

    result = client.execute_query(PROTECTED_VMS_QUERY)

    vms = result["data"]["vSphereVmNewConnection"]["nodes"]

    total_vms = len(vms)
    protected = 0
    unprotected = 0
    do_not_protect = 0

    for vm in vms:

        sla = vm["effectiveSlaDomain"]["name"]

        if sla == "UNPROTECTED":
            unprotected += 1

        elif sla == "DO_NOT_PROTECT":
            do_not_protect += 1

        else:
            protected += 1

    print("\nProtection Summary")
    print("-" * 50)
    print(f"Total VMs        : {total_vms}")
    print(f"Protected VMs    : {protected}")
    print(f"Unprotected VMs  : {unprotected}")
    print(f"Do Not Protect   : {do_not_protect}")


def get_latest_recovery_points():
    result = client.execute_query(LATEST_RECOVERY_POINT_QUERY)

    vms = result["data"]["vSphereVmNewConnection"]["nodes"]

    print("\nLatest Recovery Points")
    print("-" * 50)

    for vm in vms:

        snapshot = vm["newestSnapshot"]

        if snapshot:
            print(f"{vm['name']} - No Recovery Point")

        else:
            print(f"{vm['name']} - {snapshot['date']}")


def get_vm_recovery_point (vm_name):
    result = client.execute_query(LATEST_RECOVERY_POINT_QUERY)

    vms = result["data"]["vSphereVmNewConnection"]["nodes"]

    for vm in vms:

        if vm["name"].lower() == vm_name.lower():

            snapshot = vm["newestSnapshot"]

            if snapshot:
                return f"{vm_name} - No Recovery Point"

            else:
                return f"{vm_name} - Recovery Point ID: {snapshot['id']}, Date: {snapshot['date']}"

    return f"{vm_name} not found."



# Use Case 1
get_protected_vms()

# Use Case 2
print(check_vm_protection("draas-win-vm1"))

#Use Case 3
get_unprotected_vms()

#Use Case 4
get_protection_summary()

#Use case 5
get_latest_recovery_points()

#Use case 6
print(get_vm_recovery_point("draas-win-vm1"))

