from utilities.testing import ViewTestCases, create_tags
from netbox_device_groups.models import DeviceGroupType


class DeviceGroupTypeTestCase(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkImportObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    model = DeviceGroupType

    def _get_base_url(self):
        return "plugins:{}:{}_{{}}".format(self.model._meta.app_label, self.model._meta.model_name)

    @classmethod
    def setUpTestData(cls):
        cluster_types = (
            DeviceGroupType(name="Device Group Type 1", description="A new test device group type-1"),
            DeviceGroupType(name="Device Group Type 2", description="A new test device group type-2"),
            DeviceGroupType(name="Device Group Type 3", description="A new test device group type-3"),
        )
        DeviceGroupType.objects.bulk_create(cluster_types)

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "Device Group Type X",
            "description": "A new device group type",
            "tags": [t.pk for t in tags],
        }

        cls.csv_data = (
            "name,description",
            "Device Group Type 4,Fourth device group type",
            "Device Group Type 5,Fifth device group type",
            "Device Group Type 6,Sixth device group type",
        )

        cls.csv_update_data = (
            "id,name,description",
            f"{cluster_types[0].pk},Device Group Type 7,Fourth device group type7",
            f"{cluster_types[1].pk},Device Group Type 8,Fifth device group type8",
            f"{cluster_types[2].pk},Device Group Type 9,Sixth device group type9",
        )

        cls.bulk_edit_data = {
            "description": "New description",
        }
