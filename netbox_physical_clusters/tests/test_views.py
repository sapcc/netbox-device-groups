from utilities.testing import ViewTestCases, create_tags
from netbox_physical_clusters.models import PhysicalClusterType


class PhysicalClusterTypeTestCase(
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.BulkImportObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    model = PhysicalClusterType

    def _get_base_url(self):
        return "plugins:{}:{}_{{}}".format(self.model._meta.app_label, self.model._meta.model_name)

    @classmethod
    def setUpTestData(cls):
        cluster_types = (
            PhysicalClusterType(name="Cluster Type 1", description="A new test cluster type-1"),
            PhysicalClusterType(name="Cluster Type 2", description="A new test cluster type-2"),
            PhysicalClusterType(name="Cluster Type 3", description="A new test cluster type-3"),
        )
        PhysicalClusterType.objects.bulk_create(cluster_types)

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "Cluster Type X",
            "description": "A new cluster type",
            "tags": [t.pk for t in tags],
        }

        cls.csv_data = (
            "name,description",
            "Cluster Type 4,Fourth cluster type",
            "Cluster Type 5,Fifth cluster type",
            "Cluster Type 6,Sixth cluster type",
        )

        cls.csv_update_data = (
            "id,name,description",
            f"{cluster_types[0].pk},Cluster Type 7,Fourth cluster type7",
            f"{cluster_types[1].pk},Cluster Type 8,Fifth cluster type8",
            f"{cluster_types[2].pk},Cluster Type 9,Sixth cluster type9",
        )

        cls.bulk_edit_data = {
            "description": "New description",
        }
