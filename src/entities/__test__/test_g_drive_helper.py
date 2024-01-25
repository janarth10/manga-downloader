from g_drive_helper import (
  get_google_drive_service,
  upload_file_to_drive
)

# class TestGDriveHelper(TestCase):
#   @mock.patch('g_drive_helper.build')
#   def test_get_google_drive_service(self, mock_build):
#     # Mock the build function to return a mock service
#     mock_service = mock.Mock(spec=Resource)
#     mock_build.return_value = mock_service

#     # Call the function under test
#     service = get_google_drive_service()

#     # Assertions
#     self.assertEqual(service, mock_service)
#     mock_build.assert_called_once_with('drive', 'v3', credentials=mock.ANY)

# if __name__ == '__main__':
#   unittest.main()


def test_get_google_drive_service():
    service = get_google_drive_service()

def can_I_read_files():
    service = get_google_drive_service()
    
    results = (
        service.files()
        .list(pageSize=10, fields="nextPageToken, files(id, name)")
        .execute()
    )
    items = results.get("files", [])
    assert(len(items) > 0)

def test_upload_file_to_drive():
    ONE_PIECE_FOLDER_ID = "1qrHhGErUjHzhyVUsLelz11Z_88-XpmCL"

    file_data = upload_file_to_drive(
        drive_file_name="TEST_one_piece_1098.pdf",
        file_path="/Users/janarth.punniyamoorthyopendoor.com/personal-git/manga-downloader/one_piece_1098.pdf",
        parents=[ONE_PIECE_FOLDER_ID]
    )
    assert(file_data["name"] == "TEST_one_piece_1098.pdf")
